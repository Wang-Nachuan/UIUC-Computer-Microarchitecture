package boom.lsu

import chisel3._
import chisel3.util._

import freechips.rocketchip.config.Parameters
import freechips.rocketchip.diplomacy._
import freechips.rocketchip.tilelink._
import freechips.rocketchip.tile._
import freechips.rocketchip.util._
import freechips.rocketchip.rocket._

import boom.common._
import boom.exu.BrResolutionInfo
import boom.util.{IsKilledByBranch, GetNewBrMask, BranchKillableQueue, IsOlder, UpdateBrMask}

class LocalityTableEntry(implicit p: Parameters) extends BoomModule()(p)
{
    val io = IO(new Bundle {
        val init = Input(Bool())        // True - initialize this entry for a new instruction
        val update = Input(Bool())      // True - update this entry when a new memory access of same instruction occur
        val addr = Input(UInt(coreMaxAddrBits.W))   // Address of data to be accessed, should be valid when either "init" or "update" is true
        val pred = Output(UInt(1.W))    // Locality prediction: 0 - temporal, 1 - spatial
    })

    val (st_trans :: st_steady :: Nil) = Enum(2)

    val last_addr = RegInit(0.U(coreMaxAddrBits.W)) // Last data address referenced by this instruction
    val stride = RegInit(0.U(coreMaxAddrBits.W))    // The difference between two latest addresses referenced
    val length = RegInit(1.U(4.W))                  // Number of accesses with same stride
    val state = RegInit(st_trans)                   // Behavior of instruction according to its stride      
    val state_next = WireInit(state)

    val MAX_SPATIAL_STRIDE = 16.U       // TODO: Teplace this with the spatial cache line size
    val MIN_MOSTLYONE_LENGTH = 4.U      // TODO: Find a appropriate length

    state_next := state

    when (io.init) {
        last_addr := io.addr
        stride := 0.U
        length := 1.U
        state_next := st_trans
    } .elsewhen (io.update) {
        last_addr := io.addr
        stride := io.addr - last_addr
        // Update length
        when (io.addr - last_addr === stride) {
            when (length =/= (1.U << 4) - 1.U) {
                length := length + 1.U
            }
        } .otherwise {
            length := 1.U
        }
        // Update state
        when (state === st_trans) {
            when (io.addr - last_addr === stride && stride =/= 0.U) {
                state_next := st_steady
            }
        } .elsewhen (state === st_steady) {
            when (io.addr - last_addr =/= stride || io.addr - last_addr === 0.U) {
                state_next := st_trans
            }
        }
    }

    state := state_next

    when (state === st_steady) {
        when (stride < MAX_SPATIAL_STRIDE) {
            io.pred := 1.U
        } .otherwise {
            io.pred := 0.U
        }
    } .otherwise {
        when (length > MIN_MOSTLYONE_LENGTH && stride < MAX_SPATIAL_STRIDE) {
            io.pred := 1.U
        } .otherwise {
            io.pred := 0.U
        }
    }
}


class LocalityTable(implicit p: Parameters) extends BoomModule()(p)
{
    val io = IO(new Bundle {
        // Port for updating table entries
        val update_valid = Input(Bool())
        val update_inst_addr = Input(UInt(coreMaxAddrBits.W))
        val update_data_addr = Input(UInt(coreMaxAddrBits.W))
        // Port for reading prediction
        val read_valid = Input(Bool())
        val read_inst_addr = Input(UInt(coreMaxAddrBits.W))
        val read_pred = Output(UInt(1.W))
        // Signal for performance counter
        val perf_table_evict = Output(Bool())
    })

    val table_size = 64
    val inst_offset = 2
    val index_width = log2Ceil(table_size)
    val tag_width = coreMaxAddrBits - index_width - inst_offset

    // PC tag array
    val tag_array = RegInit(VecInit(Seq.fill(table_size)(0.U(tag_width.W))))
    val tag_array_valid = RegInit(VecInit(Seq.fill(table_size)(false.B)))

    // Locality entry array
    val entry_array = Array.fill(table_size)(Module(new LocalityTableEntry))

    // Update table
    // assert (io.update_inst_addr(inst_offset-1,0) === 0.U, "[locality table 1] PC must be four-byte aligned")
    val update_index = WireInit(io.update_inst_addr(inst_offset+index_width-1, inst_offset))
    val update_tag = WireInit(io.update_inst_addr(coreMaxAddrBits-1, inst_offset+index_width))

    io.perf_table_evict := false.B
    for (i <- 0 until table_size) {
        entry_array(i).io.init := false.B
        entry_array(i).io.update := false.B
        entry_array(i).io.addr := io.update_data_addr
        when (io.update_valid && update_index === i.U) {
            when (tag_array_valid(i) && tag_array(i) === update_tag) { // If hit, update the entry
                entry_array(i).io.update := true.B
            } .otherwise {  // If miss, reset the entry and tag
                entry_array(i).io.init := true.B
                tag_array(i) := update_tag
                tag_array_valid(i) := true.B
                io.perf_table_evict := true.B
            }
        }
    }

    // Read table
    // assert (io.read_inst_addr(inst_offset-1,0) === 0.U, "[locality table 2] PC must be four-byte aligned")
    val read_index = WireInit(io.read_inst_addr(inst_offset+index_width-1, inst_offset))
    val read_tag = WireInit(io.read_inst_addr(coreMaxAddrBits-1, inst_offset+index_width))

    io.read_pred := 0.U
    for (i <- 0 until table_size) {
        when (io.read_valid && read_index === i.U) {
            when (tag_array_valid(i) && tag_array(i) === read_tag) {
                io.read_pred := entry_array(i).io.pred
            }
        }
    }

}