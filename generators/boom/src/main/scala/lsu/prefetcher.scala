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
abstract class LAPrefetcherIO(implicit edge: TLEdgeOut, p: Parameters) extends BoomModule()(p)
{
  val io = IO(new Bundle {
    val lsu = Flipped(new PrefetchIO())
    val prefetch = Decoupled(new BoomDCacheReq)
  })
}

class LAPrefetcher(implicit edge: TLEdgeOut, p: Parameters) extends LAPrefetcherIO
{
  val req_valid = RegInit(false.B)
  val req_addr  = Reg(UInt(coreMaxAddrBits.W))
  
  // 1 if physical address is ready but instruction not fired to memroy
  val addr_val = io.lsu.ldq.map(s => s.valid && s.bits.addr.valid && !s.bits.addr_is_virtual && !s.bits.executed) ++ io.lsu.stq.map(s => s.valid && s.bits.addr.valid && !s.bits.addr_is_virtual)
  val addr = io.lsu.ldq.map(s => s.bits.addr.bits) ++ io.lsu.stq.map(s => s.bits.addr.bits)
  val is_prefetched = io.lsu.ldq.map(s => s.bits.prefetch_fired) ++ io.lsu.stq.map(s => s.bits.prefetch_fired)
  val fire_prefetch = Wire(Vec(numLdqEntries + numStqEntries, Bool()))
  var break = false.B
  var idx = 0

  for (i <- 0 until numLdqEntries + numStqEntries) {
    fire_prefetch(i) := false.B
    when (!break && addr_val(i) && !is_prefetched(i)) {
      break = true.B
      idx = i
    }
  }

  when (break && !req_valid) {
    req_valid := true.B
    req_addr  := addr(idx)
    fire_prefetch(idx) := true.B
  } .elsewhen (io.prefetch.fire()) {
    req_valid := false.B
  }

  io.prefetch.valid            := req_valid
  io.prefetch.bits.addr        := req_addr
  io.prefetch.bits.uop         := NullMicroOp   // ?
  io.prefetch.bits.uop.mem_cmd := M_PFR   // M_XRD (load)? M_PFR (prefetch for read)?
  io.prefetch.bits.data        := DontCare
  io.prefetch.bits.is_hella    := true.B   // ?

  io.lsu.ldq_prefetch_fired := fire_prefetch.slice(0, numLdqEntries)
  io.lsu.stq_prefetch_fired := fire_prefetch.slice(numLdqEntries, numLdqEntries + numStqEntries)
}
