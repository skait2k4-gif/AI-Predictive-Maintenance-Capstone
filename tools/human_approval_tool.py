# ============================================================
# STEP 16
# RISK-BASED HUMAN APPROVAL
# + WORK ORDER EXECUTION SIMULATION
#
# Group 16 Capstone:
# AI-Powered Predictive Maintenance &
# Intelligent Service Management
#
# PURPOSE:
# Execute the Step 15 service plan using risk-based governance.
#
# GOVERNANCE RULE:
#
# CRITICAL ALERT
#       -> HITL REQUIRED
#       -> APPROVE / MODIFY / REJECT / ESCALATE
#
# NON-CRITICAL ROUTINE ALERT
#       -> NO HITL
#       -> AUTO-AUTHORIZED
#       -> SIMULATED EXECUTION
#
# NON-CRITICAL + CONSEQUENTIAL ACTION
#       -> HITL REQUIRED
#
# IMPORTANT:
# This is a prototype simulation.
# No real machine/system action is performed.
# ============================================================

from datetime import datetime
import uuid

# Import Step 15 service orchestrator
from service_orchestrator_tool import generate_service_action_plan


# ============================================================
# 1. READ STEP 15 GOVERNANCE DECISION
# ============================================================

def get_governance_decision(service_plan):

    approval_gate = service_plan.get(
        "Approval_Gate",
        {}
    )

    hitl_required = approval_gate.get(
        "HITL_Required",
        service_plan.get(
            "HITL_Required",
            False
        )
    )

    approval_required = approval_gate.get(
        "Approval_Required",
        hitl_required
    )

    alert_severity = service_plan.get(
        "Alert_Severity",
        service_plan.get(
            "Risk_Level",
            "UNKNOWN"
        )
    )

    governance_reason = approval_gate.get(
        "Governance_Reason",
        "No governance reason available."
    )

    consequential_action = approval_gate.get(
        "Consequential_Action",
        False
    )

    return {
        "Alert_Severity":
            str(alert_severity).strip().upper(),

        "HITL_Required":
            bool(hitl_required),

        "Approval_Required":
            bool(approval_required),

        "Governance_Reason":
            governance_reason,

        "Consequential_Action":
            consequential_action
    }


# ============================================================
# 2. CREATE WORK ORDER
# ============================================================

def create_draft_work_order(service_plan):

    machine_serial = service_plan.get(
        "Machine_Serial_No",
        service_plan.get(
            "Machine",
            "UNKNOWN"
        )
    )

    governance = get_governance_decision(
        service_plan
    )

    work_order_id = (
        "WO-"
        + uuid.uuid4().hex[:8].upper()
    )

    # --------------------------------------------------------
    # CRITICAL / CONSEQUENTIAL CASE
    # --------------------------------------------------------

    if governance["HITL_Required"]:

        work_order_status = (
            "DRAFT - NOT RELEASED"
        )

        approval_status = (
            "WAITING_FOR_APPROVAL"
        )

        execution_status = (
            "BLOCKED PENDING HUMAN APPROVAL"
        )

        human_decision = None

        governance_control = (
            "Human approval is mandatory because the case is "
            "Critical or the proposed action is consequential."
        )

    # --------------------------------------------------------
    # ROUTINE NON-CRITICAL CASE
    # --------------------------------------------------------

    else:

        work_order_status = (
            "AUTO-AUTHORIZED"
        )

        approval_status = (
            "NOT REQUIRED - AUTO AUTHORIZED"
        )

        execution_status = (
            "READY FOR ROUTINE EXECUTION"
        )

        human_decision = (
            "AUTO_APPROVED"
        )

        governance_control = (
            "Non-critical routine service action is within "
            "approved agent guardrails. Manual HITL approval "
            "is not required."
        )

    work_order = {

        "Work_Order_ID":
            work_order_id,

        "Machine_Serial_No":
            machine_serial,

        "Created_Timestamp":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "Alert_Severity":
            governance[
                "Alert_Severity"
            ],

        "HITL_Required":
            governance[
                "HITL_Required"
            ],

        "Consequential_Action":
            governance[
                "Consequential_Action"
            ],

        "Work_Order_Status":
            work_order_status,

        "Approval_Status":
            approval_status,

        "Service_Plan":
            service_plan,

        "Human_Decision":
            human_decision,

        "Reviewer_Remarks":
            None,

        "Approved_By":
            None,

        "Approval_Timestamp":
            None,

        "Execution_Status":
            execution_status,

        "Governance_Reason":
            governance[
                "Governance_Reason"
            ],

        "Governance_Control":
            governance_control
    }

    return work_order


# ============================================================
# 3. DISPLAY GOVERNANCE SCREEN
# ============================================================

def display_approval_screen(work_order):

    print("\n" + "=" * 78)

    print(
        "STEP 16 - RISK-BASED EXECUTION CONTROL"
    )

    print("=" * 78)

    print("\n--- WORK ORDER ---")

    print(
        "Work Order ID       :",
        work_order[
            "Work_Order_ID"
        ]
    )

    print(
        "Machine             :",
        work_order[
            "Machine_Serial_No"
        ]
    )

    print(
        "Alert Severity      :",
        work_order[
            "Alert_Severity"
        ]
    )

    print(
        "HITL Required       :",
        work_order[
            "HITL_Required"
        ]
    )

    print(
        "Work Order Status   :",
        work_order[
            "Work_Order_Status"
        ]
    )

    print(
        "Approval Status     :",
        work_order[
            "Approval_Status"
        ]
    )

    print(
        "Execution Status    :",
        work_order[
            "Execution_Status"
        ]
    )

    print(
        "Consequential Action:",
        work_order[
            "Consequential_Action"
        ]
    )

    print(
        "Governance Reason   :",
        work_order[
            "Governance_Reason"
        ]
    )

    service_plan = work_order[
        "Service_Plan"
    ]

    # --------------------------------------------------------
    # STEP 15 SUMMARY
    # --------------------------------------------------------

    print(
        "\n--- AI / AGENTIC SERVICE PLAN SUMMARY ---"
    )

    print(
        "Risk Level          :",
        service_plan.get(
            "Risk_Level",
            "Unknown"
        )
    )

    service_priority = service_plan.get(
        "Service_Priority",
        {}
    )

    if service_priority:

        print(
            "Priority            :",
            service_priority.get(
                "Priority_Code",
                ""
            ),
            "-",
            service_priority.get(
                "Priority",
                ""
            )
        )

    agent_decision = service_plan.get(
        "Agent_Decision",
        {}
    )

    if agent_decision:

        print(
            "Agent State         :",
            agent_decision.get(
                "Agent_State",
                "Unknown"
            )
        )

        print(
            "Agent Decision      :",
            agent_decision.get(
                "Decision",
                "Unknown"
            )
        )

        print(
            "Next Action         :",
            agent_decision.get(
                "Next_Action",
                "Unknown"
            )
        )

    # --------------------------------------------------------
    # HITL REQUIRED
    # --------------------------------------------------------

    if work_order[
        "HITL_Required"
    ]:

        print(
            "\n--- HUMAN-IN-THE-LOOP CONTROL ---"
        )

        print(
            "The AI/Agent has prepared a proposed "
            "service action plan."
        )

        print(
            "The work order cannot be released until "
            "an authorized human reviewer makes a decision."
        )

        print(
            "\nAvailable Decisions:"
        )

        print(
            "1 - APPROVE"
        )

        print(
            "2 - MODIFY"
        )

        print(
            "3 - REJECT"
        )

        print(
            "4 - ESCALATE"
        )

    # --------------------------------------------------------
    # NO HITL REQUIRED
    # --------------------------------------------------------

    else:

        print(
            "\n--- AUTOMATIC ROUTINE AUTHORIZATION ---"
        )

        print(
            "This is a non-critical routine case."
        )

        print(
            "Human approval is NOT required."
        )

        print(
            "The agent is authorized to continue "
            "within the approved guardrails."
        )

        print(
            "No Approve / Modify / Reject / Escalate "
            "question will be asked."
        )

    print("=" * 78)


# ============================================================
# 4. HUMAN DECISION
# ============================================================

def human_approval(work_order):

    # --------------------------------------------------------
    # NO HITL REQUIRED
    # --------------------------------------------------------

    if not work_order[
        "HITL_Required"
    ]:

        work_order[
            "Human_Decision"
        ] = "AUTO_APPROVED"

        work_order[
            "Approval_Status"
        ] = "NOT REQUIRED - AUTO AUTHORIZED"

        work_order[
            "Reviewer_Remarks"
        ] = (
            "Routine non-critical action automatically "
            "authorized within approved guardrails."
        )

        work_order[
            "Approved_By"
        ] = "AGENT GUARDRAIL POLICY"

        work_order[
            "Approval_Timestamp"
        ] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        work_order[
            "Work_Order_Status"
        ] = "AUTO-AUTHORIZED"

        work_order[
            "Execution_Status"
        ] = "READY FOR ROUTINE EXECUTION"

        return work_order

    # --------------------------------------------------------
    # HITL REQUIRED
    # --------------------------------------------------------

    while True:

        decision = input(
            "\nEnter decision (1/2/3/4): "
        ).strip()

        # ----------------------------------------------------
        # APPROVE
        # ----------------------------------------------------

        if decision == "1":

            reviewer = input(
                "Enter reviewer name: "
            ).strip()

            remarks = input(
                "Enter approval remarks: "
            ).strip()

            if not reviewer:

                reviewer = (
                    "Authorized Technical Reviewer"
                )

            if not remarks:

                remarks = (
                    "Service plan reviewed and approved."
                )

            work_order[
                "Human_Decision"
            ] = "APPROVED"

            work_order[
                "Approval_Status"
            ] = "APPROVED"

            work_order[
                "Approved_By"
            ] = reviewer

            work_order[
                "Reviewer_Remarks"
            ] = remarks

            work_order[
                "Approval_Timestamp"
            ] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            work_order[
                "Work_Order_Status"
            ] = "RELEASED"

            work_order[
                "Execution_Status"
            ] = "READY FOR EXECUTION"

            return work_order

        # ----------------------------------------------------
        # MODIFY
        # ----------------------------------------------------

        elif decision == "2":

            reviewer = input(
                "Enter reviewer name: "
            ).strip()

            remarks = input(
                "Enter required modification: "
            ).strip()

            if not reviewer:

                reviewer = (
                    "Authorized Technical Reviewer"
                )

            if not remarks:

                remarks = (
                    "Technical modification required."
                )

            work_order[
                "Human_Decision"
            ] = "MODIFY"

            work_order[
                "Approval_Status"
            ] = (
                "RETURNED FOR MODIFICATION"
            )

            work_order[
                "Approved_By"
            ] = reviewer

            work_order[
                "Reviewer_Remarks"
            ] = remarks

            work_order[
                "Approval_Timestamp"
            ] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            work_order[
                "Work_Order_Status"
            ] = (
                "DRAFT - MODIFICATION REQUIRED"
            )

            work_order[
                "Execution_Status"
            ] = "BLOCKED"

            return work_order

        # ----------------------------------------------------
        # REJECT
        # ----------------------------------------------------

        elif decision == "3":

            reviewer = input(
                "Enter reviewer name: "
            ).strip()

            remarks = input(
                "Enter rejection reason: "
            ).strip()

            if not reviewer:

                reviewer = (
                    "Authorized Technical Reviewer"
                )

            if not remarks:

                remarks = (
                    "Service plan rejected by "
                    "technical reviewer."
                )

            work_order[
                "Human_Decision"
            ] = "REJECTED"

            work_order[
                "Approval_Status"
            ] = "REJECTED"

            work_order[
                "Approved_By"
            ] = reviewer

            work_order[
                "Reviewer_Remarks"
            ] = remarks

            work_order[
                "Approval_Timestamp"
            ] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            work_order[
                "Work_Order_Status"
            ] = "CANCELLED"

            work_order[
                "Execution_Status"
            ] = "BLOCKED"

            return work_order

        # ----------------------------------------------------
        # ESCALATE
        # ----------------------------------------------------

        elif decision == "4":

            reviewer = input(
                "Enter reviewer name: "
            ).strip()

            remarks = input(
                "Enter escalation reason: "
            ).strip()

            if not reviewer:

                reviewer = (
                    "Authorized Technical Reviewer"
                )

            if not remarks:

                remarks = (
                    "Additional senior technical "
                    "review required."
                )

            work_order[
                "Human_Decision"
            ] = "ESCALATED"

            work_order[
                "Approval_Status"
            ] = (
                "ESCALATED FOR SENIOR REVIEW"
            )

            work_order[
                "Approved_By"
            ] = reviewer

            work_order[
                "Reviewer_Remarks"
            ] = remarks

            work_order[
                "Approval_Timestamp"
            ] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            work_order[
                "Work_Order_Status"
            ] = (
                "ON HOLD - ESCALATED"
            )

            work_order[
                "Execution_Status"
            ] = "BLOCKED"

            return work_order

        else:

            print(
                "\nInvalid selection."
                "\nPlease enter 1, 2, 3 or 4."
            )


# ============================================================
# 5. SIMULATE WORK ORDER EXECUTION
# ============================================================

def simulate_execution(work_order):

    print("\n" + "=" * 78)

    print(
        "WORK ORDER EXECUTION CONTROL"
    )

    print("=" * 78)

    # --------------------------------------------------------
    # HITL CASE
    # --------------------------------------------------------

    if work_order[
        "HITL_Required"
    ]:

        if work_order[
            "Approval_Status"
        ] != "APPROVED":

            print(
                "\nEXECUTION BLOCKED"
            )

            print(
                "Reason: Required human approval "
                "has not been granted."
            )

            print(
                "Current Approval Status:",
                work_order[
                    "Approval_Status"
                ]
            )

            print(
                "\nAgent is NOT authorized to execute "
                "the consequential service action."
            )

            return work_order

        print(
            "\nHUMAN APPROVAL VERIFIED"
        )

        print(
            "Authorized By :",
            work_order[
                "Approved_By"
            ]
        )

        print(
            "Approval Time :",
            work_order[
                "Approval_Timestamp"
            ]
        )

    # --------------------------------------------------------
    # NON-HITL CASE
    # --------------------------------------------------------

    else:

        if work_order[
            "Human_Decision"
        ] != "AUTO_APPROVED":

            print(
                "\nEXECUTION BLOCKED"
            )

            print(
                "Reason: Routine authorization "
                "state could not be verified."
            )

            return work_order

        print(
            "\nROUTINE AUTO-AUTHORIZATION VERIFIED"
        )

        print(
            "Alert Severity :",
            work_order[
                "Alert_Severity"
            ]
        )

        print(
            "HITL Required  : NO"
        )

        print(
            "Authorization  :",
            work_order[
                "Approved_By"
            ]
        )

        print(
            "The case is within approved "
            "routine agent guardrails."
        )

    # --------------------------------------------------------
    # SIMULATED EXECUTION
    # --------------------------------------------------------

    print(
        "\nWork Order:",
        work_order[
            "Work_Order_ID"
        ],
        "has been released."
    )

    work_order[
        "Execution_Status"
    ] = (
        "SIMULATED WORK ORDER RELEASED"
    )

    work_order[
        "Work_Order_Status"
    ] = (
        "RELEASED FOR SERVICE EXECUTION"
    )

    print(
        "\nSIMULATED EXECUTION SUCCESSFUL"
    )

    print(
        "No real machine/system action has been performed."
    )

    print(
        "In production, this step could connect through "
        "an approved API/MCP integration to the enterprise "
        "service-management/work-order system."
    )

    return work_order


# ============================================================
# 6. DISPLAY FINAL GOVERNANCE RESULT
# ============================================================

def display_final_result(work_order):

    print("\n" + "=" * 78)

    print(
        "STEP 16 - FINAL CONTROL RESULT"
    )

    print("=" * 78)

    print(
        "Machine              :",
        work_order[
            "Machine_Serial_No"
        ]
    )

    print(
        "Alert Severity       :",
        work_order[
            "Alert_Severity"
        ]
    )

    print(
        "HITL Required        :",
        work_order[
            "HITL_Required"
        ]
    )

    print(
        "Work Order ID        :",
        work_order[
            "Work_Order_ID"
        ]
    )

    print(
        "Human Decision       :",
        work_order[
            "Human_Decision"
        ]
    )

    print(
        "Approval Status      :",
        work_order[
            "Approval_Status"
        ]
    )

    print(
        "Work Order Status    :",
        work_order[
            "Work_Order_Status"
        ]
    )

    print(
        "Execution Status     :",
        work_order[
            "Execution_Status"
        ]
    )

    print(
        "Authorized / Approved:",
        work_order[
            "Approved_By"
        ]
    )

    print(
        "Reviewer Remarks     :",
        work_order[
            "Reviewer_Remarks"
        ]
    )

    print(
        "\n--- GOVERNANCE / HITL ---"
    )

    print(
        "AI Role    : Predict / Diagnose / "
        "Recommend / Coordinate"
    )

    if work_order[
        "HITL_Required"
    ]:

        print(
            "Human Role : Validate / Approve / Modify / "
            "Reject / Escalate"
        )

        print(
            "System Role: Execute only after "
            "authorized human approval"
        )

        print(
            "\nGovernance Principle:"
        )

        print(
            "Critical or consequential service actions "
            "remain under human authority."
        )

    else:

        print(
            "Human Role : Oversight / Exception Handling"
        )

        print(
            "System Role: Execute routine action within "
            "approved guardrails"
        )

        print(
            "\nGovernance Principle:"
        )

        print(
            "Routine non-critical actions may be "
            "auto-authorized to avoid unnecessary "
            "human approval workload."
        )

    print(
        "\nAccountability remains governed by "
        "the defined service policy and authority matrix."
    )

    print("=" * 78)


# ============================================================
# 7. COMPLETE STEP 16 WORKFLOW
# ============================================================

def run_human_approval_workflow(
    machine_serial_no
):

    print("\n" + "=" * 78)

    print(
        "AI CAPSTONE - STEP 16"
    )

    print(
        "RISK-BASED HUMAN APPROVAL + "
        "WORK ORDER EXECUTION SIMULATION"
    )

    print("=" * 78)

    # --------------------------------------------------------
    # CALL STEP 15
    # --------------------------------------------------------

    print(
        "\nCalling Step 15 Service Orchestrator..."
    )

    service_plan = (
        generate_service_action_plan(
            machine_serial_no
        )
    )

    # --------------------------------------------------------
    # CREATE WORK ORDER
    # --------------------------------------------------------

    work_order = (
        create_draft_work_order(
            service_plan
        )
    )

    # --------------------------------------------------------
    # DISPLAY GOVERNANCE DECISION
    # --------------------------------------------------------

    display_approval_screen(
        work_order
    )

    # --------------------------------------------------------
    # CRITICAL / CONSEQUENTIAL
    # HUMAN APPROVAL REQUIRED
    # --------------------------------------------------------

    if work_order[
        "HITL_Required"
    ]:

        work_order = (
            human_approval(
                work_order
            )
        )

    # --------------------------------------------------------
    # ROUTINE NON-CRITICAL
    # AUTO AUTHORIZE
    # --------------------------------------------------------

    else:

        print(
            "\nNo HITL approval requested."
        )

        print(
            "Applying routine auto-authorization policy..."
        )

        work_order = (
            human_approval(
                work_order
            )
        )

    # --------------------------------------------------------
    # EXECUTION
    # --------------------------------------------------------

    work_order = (
        simulate_execution(
            work_order
        )
    )

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    display_final_result(
        work_order
    )

    return work_order


# ============================================================
# 8. PROTOTYPE SHOWCASE
# ============================================================

if __name__ == "__main__":

    # Critical showcase machine
    # Same machine used in Steps 13, 14 and 15
    machine_serial = "XYZ20T100017"

    final_work_order = (
        run_human_approval_workflow(
            machine_serial
        )
    )

    print("\n" + "=" * 78)

    print(
        "STEP 16 COMPLETE"
    )

    if final_work_order[
        "HITL_Required"
    ]:

        print(
            "Predict -> Diagnose -> Plan -> "
            "Human Approve -> Execute"
        )

    else:

        print(
            "Predict -> Diagnose -> Plan -> "
            "Auto-Authorize -> Execute"
        )

    print(
        "\nNext: Step 17 - Outcome Capture + "
        "Closed-Loop Learning"
    )

    print("=" * 78)