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

    when (state_next === st_steady) {
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

