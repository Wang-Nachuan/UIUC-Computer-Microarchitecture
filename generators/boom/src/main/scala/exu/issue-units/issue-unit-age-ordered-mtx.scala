//******************************************************************************
// Copyright (c) 2015 - 2018, The Regents of the University of California (Regents).
// All Rights Reserved. See LICENSE and LICENSE.SiFive for license details.
//------------------------------------------------------------------------------

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
// RISCV Processor Issue Logic
//------------------------------------------------------------------------------
//------------------------------------------------------------------------------

package boom.exu

import chisel3._
import chisel3.util.{log2Ceil, PopCount}

import freechips.rocketchip.config.Parameters
import freechips.rocketchip.util.Str

import FUConstants._
import boom.common._

import scala.util.control.Breaks._
import chisel3.util.Cat

/**
 * Specific type of issue unit
 *
 * @param params issue queue params
 * @param numWakeupPorts number of wakeup ports for the issue queue
 */
class IssueUnitAgeMatrix(
  params: IssueParams,
  numWakeupPorts: Int)
  (implicit p: Parameters)
  extends IssueUnit(params.numEntries, params.issueWidth, numWakeupPorts, params.iqType, params.dispatchWidth)
{
  //-------------------------------------------------------------
  // Dispatch/Entry Logic
  // did we find a spot to slide the new dispatched uops into?

  val free_for_dispatch = (0 until numIssueSlots).map(i => (!issue_slots(i).will_be_valid || issue_slots(i).clear))
  val will_be_available = (0 until numIssueSlots).map(i => (!issue_slots(i).will_be_valid || issue_slots(i).clear) && !(issue_slots(i).in_uop.valid))
  val num_available = PopCount(will_be_available)
  for (w <- 0 until dispatchWidth) {
    io.dis_uops(w).ready := RegNext(num_available > w.U)
  }
  
  //-------------------------------------------------------------
  
  // which entries' uops will still be next cycle? (not being issued and vacated)
  val will_be_valid_dis = (0 until dispatchWidth).map(i => io.dis_uops(i).valid &&
    !dis_uops(i).exception &&
    !dis_uops(i).is_fence &&
    !dis_uops(i).is_fencei
  )

  // Map newly dispatched instructions to free slots
  val dis_idx = Wire(Vec(dispatchWidth, UInt(log2Ceil(numIssueSlots).W)))
  dis_idx.foreach {idx => idx := 0.U}
  val dis_idx_valid = WireInit(VecInit(Seq.fill(dispatchWidth)(false.B)))
  for (i <- 0 until dispatchWidth) {
    if (i == 0) {
      var is_break = false.B
      for (j <- 0 until numIssueSlots) {
        when (will_be_valid_dis(i) && free_for_dispatch(j) && !is_break) {
          dis_idx(i) := j.U
          dis_idx_valid(i) := true.B
        }
        is_break = (will_be_valid_dis(i) && free_for_dispatch(j)) | is_break
      }
    } else {
      var is_break = false.B
      for (j <- 0 until numIssueSlots) {
        when (will_be_valid_dis(i) && j.U > dis_idx(i-1) && dis_idx_valid(i-1) && free_for_dispatch(j) && !is_break) {
          dis_idx(i) := j.U
          dis_idx_valid(i) := true.B
        }
        is_break = (will_be_valid_dis(i) && j.U > dis_idx(i-1) && dis_idx_valid(i-1) && free_for_dispatch(j)) | is_break
      }
    }
  }

  // Dispatch instructions
  for (i <- 0 until numIssueSlots) {
    issue_slots(i).in_uop.valid := false.B
    issue_slots(i).in_uop.bits := NullMicroOp
    var is_break = false.B
    for (j <- 0 until dispatchWidth) {
      when (dis_idx_valid(j) && dis_idx(j) === i.U && !is_break) {
        issue_slots(i).in_uop.valid := true.B
        issue_slots(i).in_uop.bits := dis_uops(j)
      }
      is_break = (dis_idx_valid(j) && dis_idx(j) === i.U) | is_break
    }
    issue_slots(i).clear := false.B   // ?
  }
  
  //-------------------------------------------------------------

  // Age matrix
  val age_mtx_reg = RegInit(VecInit(Seq.fill(numIssueSlots)(0.U(numIssueSlots.W))))
  
  // Update matrix at dispatch
  for (i <- 0 until dispatchWidth) {
    when (will_be_valid_dis(i)) {
      age_mtx_reg(dis_idx(i)) := VecInit(free_for_dispatch.map(!_)).asUInt
      for (j <- 0 until i) {
        when (will_be_valid_dis(j)) {
          age_mtx_reg(dis_idx(i)) := age_mtx_reg(dis_idx(i)) | (1.U(numIssueSlots.W) << dis_idx(j))  
        }
      }
    }
  }

  // Update matrix at issue
  val iss_idx_valid = WireInit(VecInit(Seq.fill(issueWidth)(false.B)))
  val iss_idx = WireInit(VecInit(Seq.fill(issueWidth)(0.U(log2Ceil(numIssueSlots).W))))
  for (i <- 0 until issueWidth) {
    when (iss_idx_valid(i)) {
      for (j <- 0 until numIssueSlots) {
        age_mtx_reg(j) := age_mtx_reg(j) & (~(1.U(numIssueSlots.W) << iss_idx(i)))
      }
    }
  }

  //-------------------------------------------------------------
  // Issue Select Logic

  // set default
  for (w <- 0 until issueWidth) {
    io.iss_valids(w) := false.B
    io.iss_uops(w)   := NullMicroOp
    // unsure if this is overkill
    io.iss_uops(w).prs1 := 0.U
    io.iss_uops(w).prs2 := 0.U
    io.iss_uops(w).prs3 := 0.U
    io.iss_uops(w).lrs1_rtype := RT_X
    io.iss_uops(w).lrs2_rtype := RT_X
  }

  val requests = issue_slots.map(s => s.request)
  val port_issued = Array.fill(issueWidth){Bool()}
  for (w <- 0 until issueWidth) {
    port_issued(w) = false.B
  }

  for (i <- 0 until numIssueSlots) {
    issue_slots(i).grant := false.B
  }

  val slot_age = age_mtx_reg.map(s => PopCount(s))  // Smaller -> older
  var curr_age = 0.U
  for (w <- 0 until issueWidth) {
    for (i <- 0 until numIssueSlots) {
      val can_allocate = (issue_slots(i).uop.fu_code & io.fu_types(w)) =/= 0.U
      // Age match && Inst ready to issue && Exe unit available && Port idle
      when (slot_age(i) === curr_age && requests(i) && can_allocate && !port_issued(w)) {
        issue_slots(i).grant := true.B
        io.iss_valids(w) := true.B
        io.iss_uops(w) := issue_slots(i).uop
        iss_idx(curr_age) := i.U
        iss_idx_valid(curr_age) := true.B
      }
      curr_age = curr_age + (slot_age(i) === curr_age && requests(i) && can_allocate && !port_issued(w))
      port_issued(w) = (slot_age(i) === curr_age && requests(i) && can_allocate) | port_issued(w)
    }
  }
}
