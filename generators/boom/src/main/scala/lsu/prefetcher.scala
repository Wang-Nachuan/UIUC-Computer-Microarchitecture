//******************************************************************************
// See LICENSE.Berkeley for license details.
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------

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



abstract class DataPrefetcher(implicit edge: TLEdgeOut, p: Parameters) extends BoomModule()(p)
{
  val io = IO(new Bundle {
    val mshr_avail = Input(Bool())
    val req_val    = Input(Bool())
    val req_addr   = Input(UInt(coreMaxAddrBits.W))
    val req_coh    = Input(new ClientMetadata)

    val prefetch   = Decoupled(new BoomDCacheReq)
  })
}

/**
  * Does not prefetch
  */
class NullPrefetcher(implicit edge: TLEdgeOut, p: Parameters) extends DataPrefetcher
{
  io.prefetch.valid := false.B
  io.prefetch.bits  := DontCare
}

/**
  * Next line prefetcher. Grabs the next line on a cache miss
  */
class NLPrefetcher(implicit edge: TLEdgeOut, p: Parameters) extends DataPrefetcher
{

  val req_valid = RegInit(false.B)
  val req_addr  = Reg(UInt(coreMaxAddrBits.W))
  val req_cmd   = Reg(UInt(M_SZ.W))

  val mshr_req_addr = io.req_addr + cacheBlockBytes.U
  val cacheable = edge.manager.supportsAcquireBSafe(mshr_req_addr, lgCacheBlockBytes.U)
  when (io.req_val && cacheable) {
    req_valid := true.B
    req_addr  := mshr_req_addr
    req_cmd   := Mux(ClientStates.hasWritePermission(io.req_coh.state), M_PFW, M_PFR)
  } .elsewhen (io.prefetch.fire()) {
    req_valid := false.B
  }

  io.prefetch.valid            := req_valid && io.mshr_avail
  io.prefetch.bits.addr        := req_addr
  io.prefetch.bits.uop         := NullMicroOp
  io.prefetch.bits.uop.mem_cmd := req_cmd
  io.prefetch.bits.data        := DontCare


}

/**
  * Look-ahead prefetcher. Try to prefetch for each instruction whose physical address is ready
  */
class PrefetchIO(implicit p: Parameters) extends BoomBundle()(p)
{
  val ldq = Input(Vec(numLdqEntries, Valid(new LDQEntry)))
  val stq = Input(Vec(numStqEntries, Valid(new STQEntry)))

  val ldq_head = Input(UInt(ldqAddrSz.W))
  val ldq_tail = Input(UInt(ldqAddrSz.W))
  val stq_head = Input(UInt(stqAddrSz.W)) // point to next store to clear from STQ (i.e., send to memory)
  val stq_tail = Input(UInt(stqAddrSz.W))
  val stq_commit_head = Input(UInt(stqAddrSz.W)) // point to next store to commit
  val stq_execute_head = Input(UInt(stqAddrSz.W)) // point to next store to execute
  
  val ldq_prefetch_fired = Output(Vec(numLdqEntries, Bool()))
  val stq_prefetch_fired = Output(Vec(numStqEntries, Bool()))

  val perf_prefetch_commit = Output(Bool())
  val perf_prefetch_fire = Output(Bool())
}

abstract class LAPrefetcherIO(implicit edge: TLEdgeOut, p: Parameters) extends BoomModule()(p)
{
  val io = IO(new Bundle {
    val lsu = new PrefetchIO()
    val prefetch = Valid(new BoomDCacheReq)
  })
}

class LAPrefetcher(implicit edge: TLEdgeOut, p: Parameters) extends LAPrefetcherIO
{
  val req_valid = RegInit(false.B)
  val req_addr = RegInit(0.U(coreMaxAddrBits.W))

  // Find a entry to prefetch in LDQ
  val ldq_addr_ready = io.lsu.ldq.map(s => s.valid && s.bits.addr.valid && !s.bits.addr_is_virtual)
  val ldq_addr = io.lsu.ldq.map(s => s.bits.addr.bits)
  val ldq_prefetch_fired =  io.lsu.ldq.map(s => s.bits.prefetch_fired)
  val ldq_executed = io.lsu.ldq.map(s => s.bits.executed)
  val ldq_fire_prefetch = Wire(Vec(numLdqEntries, Bool()))
  var ldq_break = false.B
  var ldq_idx = 0.U

  ldq_fire_prefetch := VecInit(Seq.fill(numLdqEntries)(false.B))
  for (i <- 0 until numLdqEntries) {
    var idx = (i.U + io.lsu.ldq_head) % numLdqEntries.U
    when (!ldq_break && ldq_addr_ready(idx) && !ldq_prefetch_fired(idx) && !ldq_executed(idx)) {
      ldq_break = true.B
      ldq_idx = idx
    }
  }
 
  // Find a entry to prefetch in STQ
  val stq_addr_ready = io.lsu.stq.map(s => s.valid && s.bits.addr.valid && !s.bits.addr_is_virtual)
  val stq_addr = io.lsu.stq.map(s => s.bits.addr.bits)
  val stq_prefetch_fired =  io.lsu.stq.map(s => s.bits.prefetch_fired)
  val stq_fire_prefetch = Wire(Vec(numStqEntries, Bool()))
  var stq_break = false.B
  var stq_idx = 0.U

  stq_fire_prefetch := VecInit(Seq.fill(numStqEntries)(false.B))
  for (i <- 0 until numStqEntries) {
    var idx = (i.U + io.lsu.stq_head) % numStqEntries.U
    when (!stq_break && stq_addr_ready(idx) && !stq_prefetch_fired(idx)) {
      stq_break = true.B
      stq_idx = idx
    }
  }

  // Arbit between two entries
  when (ldq_break && !req_valid) {
    req_valid := true.B
    req_addr := ldq_addr(ldq_idx)
    ldq_fire_prefetch(ldq_idx) := true.B
  } .elsewhen (stq_break && !req_valid) {
    req_valid := true.B
    req_addr := stq_addr(stq_idx)
    stq_fire_prefetch(stq_idx) := true.B
  } .elsewhen (io.prefetch.fire()) {
    req_valid := false.B
  }

  io.prefetch.valid            := req_valid
  io.prefetch.bits.addr        := req_addr
  io.prefetch.bits.uop         := NullMicroOp
  io.prefetch.bits.uop.mem_cmd := M_XRD   // M_XRD (load)? M_PFR (prefetch for read)?
  io.prefetch.bits.data        := DontCare
  io.prefetch.bits.is_hella    := false.B

  io.lsu.ldq_prefetch_fired := ldq_fire_prefetch
  io.lsu.stq_prefetch_fired := stq_fire_prefetch

  io.lsu.perf_prefetch_commit := (ldq_break || stq_break) && (!req_valid)
  io.lsu.perf_prefetch_fire := io.prefetch.fire()
}
