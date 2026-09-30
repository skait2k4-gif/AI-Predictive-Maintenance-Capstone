# ============================================================
# STEP 17
# OUTCOME CAPTURE + CLOSED-LOOP LEARNING
#
# Group 16 Capstone:
# AI-Powered Predictive Maintenance &
# Intelligent Service Management
#
# PURPOSE:
# Connect Step 16 execution with actual service outcome capture
# and controlled AI learning.
#
# SUPPORTS BOTH GOVERNANCE PATHS:
#
# CRITICAL / CONSEQUENTIAL
#   -> HITL
#   -> Human Approval
#   -> Execute
#   -> Capture Outcome
#   -> Learn
#
# NON-CRITICAL ROUTINE
#   -> Auto-Authorize
#   -> Execute
#   -> Capture Outcome
#   -> Learn
#
# IMPORTANT:
# This is a synthetic / academic prototype.
# No real ML retraining or production-system update occurs.
# ============================================================

from datetime import datetime
import uuid

# Import Step 16 complete workflow
from human_approval_tool import run_human_approval_workflow


# ============================================================
# 1. CREATE OUTCOME RECORD FROM STEP 16 WORK ORDER
# ============================================================

def create_outcome_record(work_order):

    outcome_id = (
        "OUT-"
        + uuid.uuid4().hex[:8].upper()
    )

    outcome = {

        "Outcome_ID":
            outcome_id,

        "Machine_Serial_No":
            work_order.get(
                "Machine_Serial_No",
                "UNKNOWN"
            ),

        "Captured_Timestamp":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "Work_Order_ID":
            work_order.get(
                "Work_Order_ID",
                "UNKNOWN"
            ),

        "Alert_Severity":
            work_order.get(
                "Alert_Severity",
                "UNKNOWN"
            ),

        "HITL_Required":
            work_order.get(
                "HITL_Required",
                False
            ),

        "Authorization_Path":
            None,

        "Human_Decision":
            work_order.get(
                "Human_Decision",
                None
            ),

        "Authorized_By":
            work_order.get(
                "Approved_By",
                None
            ),

        "Execution_Status":
            work_order.get(
                "Execution_Status",
                "UNKNOWN"
            ),

        "Actual_Finding":
            None,

        "Root_Cause":
            None,

        "Action_Taken":
            None,

        "Machine_Restored":
            None,

        "Repeat_Issue":
            None,

        "AI_Alert_Valid":
            None,

        "AI_Recommendation_Useful":
            None,

        "Technician_Feedback":
            None,

        "ML_Feedback":
            None,

        "RAG_Feedback":
            None,

        "Agent_Feedback":
            None,

        "Governance_Feedback":
            None,

        "Learning_Status":
            "NOT YET PROCESSED",

        "Data_Type":
            "Synthetic / Prototype"
    }

    # --------------------------------------------------------
    # DETERMINE AUTHORIZATION PATH
    # --------------------------------------------------------

    if outcome["HITL_Required"]:

        outcome[
            "Authorization_Path"
        ] = "HUMAN_APPROVED"

    else:

        outcome[
            "Authorization_Path"
        ] = "AUTO_AUTHORIZED"

    return outcome


# ============================================================
# 2. YES / NO INPUT HELPER
# ============================================================

def ask_yes_no(question):

    while True:

        answer = input(
            f"{question} (Y/N): "
        ).strip().upper()

        if answer in [
            "Y",
            "YES"
        ]:

            return "YES"

        elif answer in [
            "N",
            "NO"
        ]:

            return "NO"

        else:

            print(
                "Please enter Y or N."
            )


# ============================================================
# 3. CHECK WHETHER STEP 16 EXECUTED SUCCESSFULLY
# ============================================================

def execution_is_valid(work_order):

    execution_status = str(
        work_order.get(
            "Execution_Status",
            ""
        )
    ).upper()

    valid_execution_states = [
        "SIMULATED WORK ORDER RELEASED",
        "RELEASED FOR SERVICE EXECUTION",
        "EXECUTED",
        "COMPLETED"
    ]

    for state in valid_execution_states:

        if state in execution_status:

            return True

    return False


# ============================================================
# 4. CAPTURE ACTUAL SERVICE OUTCOME
# ============================================================

def capture_service_outcome(outcome):

    print(
        "\n"
        + "=" * 78
    )

    print(
        "STEP 17 - SERVICE OUTCOME CAPTURE"
    )

    print(
        "=" * 78
    )

    print(
        "\nMachine:",
        outcome[
            "Machine_Serial_No"
        ]
    )

    print(
        "Outcome ID:",
        outcome[
            "Outcome_ID"
        ]
    )

    print(
        "Work Order ID:",
        outcome[
            "Work_Order_ID"
        ]
    )

    print(
        "Alert Severity:",
        outcome[
            "Alert_Severity"
        ]
    )

    print(
        "HITL Required:",
        outcome[
            "HITL_Required"
        ]
    )

    print(
        "Authorization Path:",
        outcome[
            "Authorization_Path"
        ]
    )

    print(
        "Execution Status:",
        outcome[
            "Execution_Status"
        ]
    )

    print(
        "\n--- ACTUAL SERVICE RESULT ---"
    )

    # --------------------------------------------------------
    # ACTUAL FINDING
    # --------------------------------------------------------

    actual_finding = input(
        "\nActual finding "
        "(press Enter for prototype example): "
    ).strip()

    if not actual_finding:

        actual_finding = (
            "Cooling pack found heavily clogged "
            "with dust/debris."
        )

    outcome[
        "Actual_Finding"
    ] = actual_finding

    # --------------------------------------------------------
    # ROOT CAUSE
    # --------------------------------------------------------

    root_cause = input(
        "Confirmed root cause "
        "(press Enter for prototype example): "
    ).strip()

    if not root_cause:

        root_cause = (
            "Restricted heat rejection due to "
            "cooling pack contamination."
        )

    outcome[
        "Root_Cause"
    ] = root_cause

    # --------------------------------------------------------
    # ACTION TAKEN
    # --------------------------------------------------------

    action_taken = input(
        "Action taken "
        "(press Enter for prototype example): "
    ).strip()

    if not action_taken:

        action_taken = (
            "Cooling pack cleaned and inspected; "
            "cooling system condition verified."
        )

    outcome[
        "Action_Taken"
    ] = action_taken

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    print(
        "\n--- VALIDATION ---"
    )

    outcome[
        "Machine_Restored"
    ] = ask_yes_no(
        "Machine restored to normal operation?"
    )

    outcome[
        "Repeat_Issue"
    ] = ask_yes_no(
        "Repeat issue observed?"
    )

    # --------------------------------------------------------
    # AI VALIDATION
    # --------------------------------------------------------

    print(
        "\n--- AI VALIDATION ---"
    )

    outcome[
        "AI_Alert_Valid"
    ] = ask_yes_no(
        "Was the AI / telematics alert valid?"
    )

    outcome[
        "AI_Recommendation_Useful"
    ] = ask_yes_no(
        "Was the AI diagnostic recommendation useful?"
    )

    # --------------------------------------------------------
    # TECHNICIAN FEEDBACK
    # --------------------------------------------------------

    feedback = input(
        "\nTechnician feedback "
        "(press Enter for prototype example): "
    ).strip()

    if not feedback:

        feedback = (
            "AI recommendation correctly prioritized "
            "the relevant system inspection."
        )

    outcome[
        "Technician_Feedback"
    ] = feedback

    return outcome


# ============================================================
# 5. GENERATE CONTROLLED LEARNING FEEDBACK
# ============================================================

def generate_learning_feedback(outcome):

    # --------------------------------------------------------
    # ML FEEDBACK
    # --------------------------------------------------------

    if outcome[
        "AI_Alert_Valid"
    ] == "YES":

        outcome[
            "ML_Feedback"
        ] = (
            "POSITIVE LABEL - Predicted/identified risk "
            "was validated by actual field outcome."
        )

    else:

        outcome[
            "ML_Feedback"
        ] = (
            "REVIEW LABEL - Alert was not validated by "
            "the field outcome. Candidate false positive "
            "for controlled model review."
        )

    # --------------------------------------------------------
    # RAG / KNOWLEDGE FEEDBACK
    # --------------------------------------------------------

    if outcome[
        "AI_Recommendation_Useful"
    ] == "YES":

        outcome[
            "RAG_Feedback"
        ] = (
            "POSITIVE FEEDBACK - Retrieved diagnostic "
            "knowledge was useful to the technician."
        )

    else:

        outcome[
            "RAG_Feedback"
        ] = (
            "KNOWLEDGE REVIEW REQUIRED - Retrieved guidance "
            "was not sufficiently useful. Review retrieval, "
            "document coverage, relevance and knowledge quality."
        )

    # --------------------------------------------------------
    # AGENT / SERVICE PLAN FEEDBACK
    # --------------------------------------------------------

    if (
        outcome[
            "Machine_Restored"
        ] == "YES"
        and
        outcome[
            "Repeat_Issue"
        ] == "NO"
    ):

        outcome[
            "Agent_Feedback"
        ] = (
            "SERVICE PLAN EFFECTIVE - Intervention resulted "
            "in restoration without observed repeat issue."
        )

    elif (
        outcome[
            "Machine_Restored"
        ] == "YES"
    ):

        outcome[
            "Agent_Feedback"
        ] = (
            "PARTIAL SUCCESS - Machine restored, but repeat "
            "issue requires further technical review."
        )

    else:

        outcome[
            "Agent_Feedback"
        ] = (
            "SERVICE PLAN REVIEW REQUIRED - Machine was not "
            "successfully restored."
        )

    # --------------------------------------------------------
    # GOVERNANCE FEEDBACK
    # --------------------------------------------------------

    if outcome[
        "HITL_Required"
    ]:

        outcome[
            "Governance_Feedback"
        ] = (
            "HITL PATH VALIDATED - Critical/consequential "
            "case was routed through authorized human "
            "decision before execution."
        )

    else:

        outcome[
            "Governance_Feedback"
        ] = (
            "AUTO-AUTHORIZATION PATH VALIDATED - "
            "Non-critical routine case proceeded within "
            "approved agent guardrails without unnecessary "
            "manual approval."
        )

    # --------------------------------------------------------
    # LEARNING STATUS
    # --------------------------------------------------------

    outcome[
        "Learning_Status"
    ] = (
        "VALIDATED FEEDBACK CAPTURED FOR CONTROLLED REVIEW"
    )

    return outcome


# ============================================================
# 6. DISPLAY SERVICE OUTCOME
# ============================================================

def display_outcome(outcome):

    print(
        "\n"
        + "=" * 78
    )

    print(
        "SERVICE OUTCOME"
    )

    print(
        "=" * 78
    )

    print(
        "Outcome ID               :",
        outcome[
            "Outcome_ID"
        ]
    )

    print(
        "Machine                  :",
        outcome[
            "Machine_Serial_No"
        ]
    )

    print(
        "Work Order               :",
        outcome[
            "Work_Order_ID"
        ]
    )

    print(
        "Alert Severity           :",
        outcome[
            "Alert_Severity"
        ]
    )

    print(
        "HITL Required            :",
        outcome[
            "HITL_Required"
        ]
    )

    print(
        "Authorization Path       :",
        outcome[
            "Authorization_Path"
        ]
    )

    print(
        "Human / Agent Decision   :",
        outcome[
            "Human_Decision"
        ]
    )

    print(
        "Authorized By            :",
        outcome[
            "Authorized_By"
        ]
    )

    print(
        "Execution Status         :",
        outcome[
            "Execution_Status"
        ]
    )

    print(
        "Actual Finding           :",
        outcome[
            "Actual_Finding"
        ]
    )

    print(
        "Confirmed Root Cause     :",
        outcome[
            "Root_Cause"
        ]
    )

    print(
        "Action Taken             :",
        outcome[
            "Action_Taken"
        ]
    )

    print(
        "Machine Restored         :",
        outcome[
            "Machine_Restored"
        ]
    )

    print(
        "Repeat Issue             :",
        outcome[
            "Repeat_Issue"
        ]
    )

    print(
        "AI Alert Valid           :",
        outcome[
            "AI_Alert_Valid"
        ]
    )

    print(
        "AI Recommendation Useful :",
        outcome[
            "AI_Recommendation_Useful"
        ]
    )

    print(
        "Technician Feedback      :",
        outcome[
            "Technician_Feedback"
        ]
    )


# ============================================================
# 7. DISPLAY CLOSED-LOOP LEARNING
# ============================================================

def display_learning_feedback(outcome):

    print(
        "\n"
        + "=" * 78
    )

    print(
        "CLOSED-LOOP AI LEARNING"
    )

    print(
        "=" * 78
    )

    print(
        "\n--- ML FEEDBACK ---"
    )

    print(
        outcome[
            "ML_Feedback"
        ]
    )

    print(
        "\n--- RAG / KNOWLEDGE FEEDBACK ---"
    )

    print(
        outcome[
            "RAG_Feedback"
        ]
    )

    print(
        "\n--- AGENT / SERVICE PLAN FEEDBACK ---"
    )

    print(
        outcome[
            "Agent_Feedback"
        ]
    )

    print(
        "\n--- GOVERNANCE FEEDBACK ---"
    )

    print(
        outcome[
            "Governance_Feedback"
        ]
    )

    print(
        "\n--- LEARNING STATUS ---"
    )

    print(
        outcome[
            "Learning_Status"
        ]
    )

    print(
        "\n"
        + "-" * 78
    )

    print(
        "IMPORTANT GOVERNANCE CONTROL:"
    )

    print(
        "This prototype captures validated feedback for "
        "controlled model/knowledge improvement."
    )

    print(
        "It does NOT automatically retrain the ML model, "
        "rewrite approved technical documents, or change "
        "service rules without review and approval."
    )

    print(
        "-" * 78
    )


# ============================================================
# 8. PREPARE LEARNING PIPELINE
# ============================================================

def prepare_learning_pipeline(outcome):

    learning_pipeline = {

        "Machine_Serial_No":
            outcome[
                "Machine_Serial_No"
            ],

        "Outcome_ID":
            outcome[
                "Outcome_ID"
            ],

        "Work_Order_ID":
            outcome[
                "Work_Order_ID"
            ],

        "Alert_Severity":
            outcome[
                "Alert_Severity"
            ],

        "HITL_Required":
            outcome[
                "HITL_Required"
            ],

        "Authorization_Path":
            outcome[
                "Authorization_Path"
            ],

        "Prediction_Feedback":
            outcome[
                "ML_Feedback"
            ],

        "Diagnostic_Feedback":
            outcome[
                "RAG_Feedback"
            ],

        "Service_Plan_Feedback":
            outcome[
                "Agent_Feedback"
            ],

        "Governance_Feedback":
            outcome[
                "Governance_Feedback"
            ],

        "Actual_Root_Cause":
            outcome[
                "Root_Cause"
            ],

        "Actual_Action":
            outcome[
                "Action_Taken"
            ],

        "Machine_Restored":
            outcome[
                "Machine_Restored"
            ],

        "Repeat_Issue":
            outcome[
                "Repeat_Issue"
            ],

        "Review_Status":
            "PENDING CONTROLLED REVIEW"
    }

    return learning_pipeline


# ============================================================
# 9. DISPLAY LEARNING PIPELINE
# ============================================================

def display_learning_pipeline(
    learning_pipeline
):

    print(
        "\n"
        + "=" * 78
    )

    print(
        "LEARNING PIPELINE"
    )

    print(
        "=" * 78
    )

    print(
        "\nOutcome Capture"
        "\n      |"
        "\n      v"
        "\nValidated Technician Feedback"
        "\n      |"
        "\n      v"
        "\nML Performance Review"
        "\n      |"
        "\n      +----> RAG Knowledge Review"
        "\n      |"
        "\n      +----> Agent Plan Review"
        "\n      |"
        "\n      +----> Governance Review"
        "\n      |"
        "\n      v"
        "\nControlled Improvement"
        "\n      |"
        "\n      v"
        "\nHuman Validation / Governance"
        "\n      |"
        "\n      v"
        "\nApproved Model / Knowledge / Rule Update"
    )

    print(
        "\nAuthorization Path:"
    )

    print(
        learning_pipeline[
            "Authorization_Path"
        ]
    )

    print(
        "\nReview Status:"
    )

    print(
        learning_pipeline[
            "Review_Status"
        ]
    )

    print(
        "=" * 78
    )


# ============================================================
# 10. DISPLAY END-TO-END WORKFLOW
# ============================================================

def display_end_to_end_workflow(outcome):

    print(
        "\n"
        + "=" * 78
    )

    print(
        "END-TO-END AI SERVICE WORKFLOW"
    )

    print(
        "=" * 78
    )

    # --------------------------------------------------------
    # CRITICAL / CONSEQUENTIAL PATH
    # --------------------------------------------------------

    if outcome[
        "HITL_Required"
    ]:

        print(
            "\nCRITICAL / CONSEQUENTIAL PATH"
        )

        print(
            "\nPredict"
            "\n   -> Diagnose"
            "\n   -> Plan"
            "\n   -> Human Approve"
            "\n   -> Execute"
            "\n   -> Capture Outcome"
            "\n   -> Learn"
        )

    # --------------------------------------------------------
    # ROUTINE NON-CRITICAL PATH
    # --------------------------------------------------------

    else:

        print(
            "\nNON-CRITICAL ROUTINE PATH"
        )

        print(
            "\nPredict"
            "\n   -> Diagnose"
            "\n   -> Plan"
            "\n   -> Auto-Authorize"
            "\n   -> Execute"
            "\n   -> Capture Outcome"
            "\n   -> Learn"
        )

    print(
        "\nGovernance Principle:"
    )

    print(
        "AI autonomy increases for routine work, "
        "while human control increases with risk "
        "and consequence."
    )

    print(
        "=" * 78
    )


# ============================================================
# 11. COMPLETE STEP 17 WORKFLOW
# ============================================================

def run_outcome_learning_workflow(
    machine_serial_no
):

    print(
        "\n"
        + "=" * 78
    )

    print(
        "AI CAPSTONE - STEP 17"
    )

    print(
        "OUTCOME CAPTURE + CLOSED-LOOP LEARNING"
    )

    print(
        "=" * 78
    )

    # --------------------------------------------------------
    # CALL STEP 16
    # --------------------------------------------------------

    print(
        "\nCalling Step 16 Risk-Based Execution Workflow..."
    )

    work_order = (
        run_human_approval_workflow(
            machine_serial_no
        )
    )

    # --------------------------------------------------------
    # VERIFY EXECUTION
    # --------------------------------------------------------

    if not execution_is_valid(
        work_order
    ):

        print(
            "\n"
            + "=" * 78
        )

        print(
            "STEP 17 STOPPED"
        )

        print(
            "=" * 78
        )

        print(
            "\nOutcome learning cannot proceed because "
            "the work order was not released/executed."
        )

        print(
            "Current Execution Status:",
            work_order.get(
                "Execution_Status",
                "UNKNOWN"
            )
        )

        print(
            "Approval Status:",
            work_order.get(
                "Approval_Status",
                "UNKNOWN"
            )
        )

        print(
            "\nThis is intentional governance behavior."
        )

        print(
            "Rejected, modified, escalated or otherwise "
            "blocked work orders must not be recorded as "
            "completed service outcomes."
        )

        print(
            "=" * 78
        )

        return None, None

    # --------------------------------------------------------
    # CREATE OUTCOME RECORD USING ACTUAL STEP 16 WO
    # --------------------------------------------------------

    outcome = (
        create_outcome_record(
            work_order
        )
    )

    # --------------------------------------------------------
    # CAPTURE FIELD OUTCOME
    # --------------------------------------------------------

    outcome = (
        capture_service_outcome(
            outcome
        )
    )

    # --------------------------------------------------------
    # GENERATE LEARNING SIGNALS
    # --------------------------------------------------------

    outcome = (
        generate_learning_feedback(
            outcome
        )
    )

    # --------------------------------------------------------
    # DISPLAY ACTUAL RESULT
    # --------------------------------------------------------

    display_outcome(
        outcome
    )

    # --------------------------------------------------------
    # DISPLAY AI LEARNING FEEDBACK
    # --------------------------------------------------------

    display_learning_feedback(
        outcome
    )

    # --------------------------------------------------------
    # PREPARE CONTROLLED LEARNING PIPELINE
    # --------------------------------------------------------

    learning_pipeline = (
        prepare_learning_pipeline(
            outcome
        )
    )

    # --------------------------------------------------------
    # DISPLAY LEARNING PIPELINE
    # --------------------------------------------------------

    display_learning_pipeline(
        learning_pipeline
    )

    # --------------------------------------------------------
    # DISPLAY CORRECT GOVERNANCE PATH
    # --------------------------------------------------------

    display_end_to_end_workflow(
        outcome
    )

    return (
        outcome,
        learning_pipeline
    )


# ============================================================
# 12. PROTOTYPE SHOWCASE
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # DEFAULT SHOWCASE:
    # Critical Engine Cooling machine
    #
    # For non-critical test, temporarily use:
    # XYZ20T100017
    # --------------------------------------------------------

    machine_serial = "XYZ20T100017"

    outcome, learning_pipeline = (
        run_outcome_learning_workflow(
            machine_serial
        )
    )

    print(
        "\n"
        + "=" * 78
    )

    if outcome is not None:

        print(
            "STEP 17 COMPLETE"
        )

        if outcome[
            "HITL_Required"
        ]:

            print(
                "\nPredict -> Diagnose -> Plan -> "
                "Human Approve -> Execute -> Learn"
            )

        else:

            print(
                "\nPredict -> Diagnose -> Plan -> "
                "Auto-Authorize -> Execute -> Learn"
            )

        print(
            "\nFULL CLOSED-LOOP SERVICE WORKFLOW COMPLETED"
        )

        if outcome[
            "HITL_Required"
        ]:

            print(
                "\nMachine -> Detect Risk -> Diagnose -> "
                "Plan Service -> Human Approval -> "
                "Execute -> Capture Outcome -> Learn"
            )

        else:

            print(
                "\nMachine -> Detect Risk -> Diagnose -> "
                "Plan Service -> Auto-Authorization -> "
                "Execute -> Capture Outcome -> Learn"
            )

        print(
            "\nNext: Step 18 - End-to-End Capstone "
            "Prototype / Management Dashboard"
        )

    else:

        print(
            "STEP 17 NOT COMPLETED"
        )

        print(
            "\nReason: Work order did not reach "
            "an executable state."
        )

    print(
        "=" * 78
    )