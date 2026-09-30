# ============================================================
# STEP 15 - INTELLIGENT SERVICE ACTION PLANNING
#            / AGENTIC ORCHESTRATION
#
# Group 16 Capstone:
# AI-Powered Predictive Maintenance &
# Intelligent Service Management
#
# PURPOSE:
# Take the diagnostic result from Step 14 and convert it into
# a controlled, actionable service plan.
#
# GOVERNANCE PRINCIPLE:
# - Critical alert -> Human-in-the-Loop approval required
# - Non-critical routine action -> Auto-authorized
# - Any consequential / safety-critical action -> HITL required
#
# The agent PREPARES and COORDINATES the action.
# Human authority is retained where risk/consequence requires it.
# ============================================================

from datetime import datetime

from diagnostic_reasoning_tool import generate_diagnostic_reasoning


# ============================================================
# 1. PRIORITY DECISION
# ============================================================

def determine_service_priority(risk_level):

    risk = str(risk_level).strip().upper()

    if risk == "CRITICAL":
        return {
            "Priority_Code": "P1",
            "Priority": "Immediate Attention",
            "Response_Strategy":
                "Prepare urgent technical intervention."
        }

    elif risk == "HIGH":
        return {
            "Priority_Code": "P2",
            "Priority": "High Priority",
            "Response_Strategy":
                "Plan earliest practical technical inspection."
        }

    elif risk == "MEDIUM":
        return {
            "Priority_Code": "P3",
            "Priority": "Planned Inspection",
            "Response_Strategy":
                "Schedule inspection during earliest suitable service window."
        }

    else:
        return {
            "Priority_Code": "P4",
            "Priority": "Monitor",
            "Response_Strategy":
                "Continue monitoring and review during routine maintenance."
        }


# ============================================================
# 2. TECHNICIAN SKILL DECISION
# ============================================================

def determine_technician_skill(risk_level, search_topic):

    risk = str(risk_level).strip().upper()
    topic = str(search_topic).strip().lower()

    if risk == "CRITICAL":
        return {
            "Skill_Level": "L3",
            "Technician_Profile":
                "Senior Technical / Diagnostic Engineer",
            "Reason":
                "Critical condition requires advanced diagnosis and "
                "human technical validation."
        }

    elif risk == "HIGH":
        return {
            "Skill_Level": "L2/L3",
            "Technician_Profile":
                "Experienced Service Engineer",
            "Reason":
                f"High-risk {topic} condition requires experienced "
                "technical inspection."
        }

    elif risk == "MEDIUM":
        return {
            "Skill_Level": "L2",
            "Technician_Profile":
                "Maintenance / Service Engineer",
            "Reason":
                "Condition requires structured inspection and validation."
        }

    else:
        return {
            "Skill_Level": "L1/L2",
            "Technician_Profile":
                "Maintenance Technician",
            "Reason":
                "Routine monitoring or maintenance support."
        }


# ============================================================
# 3. TOOLS / PREPARATION DECISION
# ============================================================

def determine_required_preparation(search_topic):

    topic = str(search_topic).strip().lower()

    if topic == "cooling":

        return {
            "Inspection_Focus":
                "Engine Cooling System",

            "Tools_Equipment": [
                "Standard service tool kit",
                "Temperature verification equipment",
                "Cooling-system inspection tools",
                "Cleaning equipment as permitted by approved procedure",
                "PPE"
            ],

            "Parts_Consumables_To_Check": [
                "Coolant / approved fluid",
                "Hoses / clamps",
                "Belts",
                "Filters if applicable",
                "Sensor / connector items if diagnosis confirms requirement"
            ]
        }

    elif topic == "air":

        return {
            "Inspection_Focus":
                "Air Intake / Filtration System",

            "Tools_Equipment": [
                "Standard service tool kit",
                "Air-intake inspection equipment",
                "Approved cleaning equipment",
                "PPE"
            ],

            "Parts_Consumables_To_Check": [
                "Air filter element",
                "Pre-cleaner items if applicable",
                "Hoses / clamps",
                "Restriction indicator / sensor if required"
            ]
        }

    elif topic == "hydraulic":

        return {
            "Inspection_Focus":
                "Hydraulic System",

            "Tools_Equipment": [
                "Standard service tool kit",
                "Approved hydraulic diagnostic equipment",
                "Temperature / pressure checking equipment",
                "PPE"
            ],

            "Parts_Consumables_To_Check": [
                "Hydraulic filters",
                "Approved hydraulic oil",
                "Hoses / seals if inspection confirms requirement"
            ]
        }

    elif topic == "electrical":

        return {
            "Inspection_Focus":
                "Electrical / Sensor System",

            "Tools_Equipment": [
                "Standard service tool kit",
                "Electrical diagnostic meter",
                "Approved diagnostic interface",
                "PPE"
            ],

            "Parts_Consumables_To_Check": [
                "Connectors",
                "Wiring repair materials",
                "Sensor if diagnosis confirms requirement",
                "Battery-related items if applicable"
            ]
        }

    else:

        return {
            "Inspection_Focus":
                "General Machine Inspection",

            "Tools_Equipment": [
                "Standard service tool kit",
                "Approved diagnostic equipment",
                "PPE"
            ],

            "Parts_Consumables_To_Check": [
                "Determine after technician inspection"
            ]
        }


# ============================================================
# 4. CUSTOMER / SITE COORDINATION
# ============================================================

def determine_site_coordination(risk_level):

    risk = str(risk_level).strip().upper()

    if risk in ["CRITICAL", "HIGH"]:

        return {
            "Customer_Contact_Required": True,
            "Site_Coordination_Required": True,

            "Recommended_Message":
                "Coordinate with customer/site representative for "
                "technical inspection and suitable machine access. "
                "Do not communicate an unverified component-failure "
                "diagnosis as confirmed."
        }

    else:

        return {
            "Customer_Contact_Required": True,
            "Site_Coordination_Required": False,

            "Recommended_Message":
                "Inform customer of planned inspection/monitoring "
                "requirement during the suitable service window."
        }


# ============================================================
# 5. CONSEQUENCE CHECK
# ============================================================

def determine_consequential_action(diagnostic_result):

    """
    Secondary governance safeguard.

    Even when the alert is not Critical, HITL should still be
    triggered if the proposed action becomes consequential or
    safety-critical.

    This prototype checks the diagnostic recommendations for
    selected high-consequence terms.
    """

    actions = diagnostic_result.get(
        "Recommended_Actions",
        []
    )

    if isinstance(actions, str):
        actions = [actions]

    combined_actions = " ".join(
        str(action).lower()
        for action in actions
    )

    consequential_terms = [
        "major component replacement",
        "engine replacement",
        "pump replacement",
        "component replacement",
        "machine shutdown",
        "shut down machine",
        "stop machine",
        "safety-critical",
        "high-cost repair"
    ]

    matched_terms = [
        term
        for term in consequential_terms
        if term in combined_actions
    ]

    return {
        "Consequential_Action": bool(matched_terms),
        "Matched_Consequence_Terms": matched_terms
    }


# ============================================================
# 6. RISK-BASED HUMAN-IN-THE-LOOP / APPROVAL GATE
# ============================================================

def determine_approval_gate(diagnostic_result):

    risk = str(
        diagnostic_result.get(
            "Risk_Level",
            "LOW"
        )
    ).strip().upper()

    consequence = determine_consequential_action(
        diagnostic_result
    )

    consequential_action = consequence[
        "Consequential_Action"
    ]

    # --------------------------------------------------------
    # RULE 1:
    # CRITICAL ALERT -> HITL REQUIRED
    # --------------------------------------------------------

    if risk == "CRITICAL":

        return {
            "Approval_Required": True,
            "HITL_Required": True,

            "Approval_Status":
                "WAITING FOR HUMAN APPROVAL",

            "Governance_Reason":
                "Critical alert requires authorized human "
                "technical approval before execution.",

            "Consequential_Action":
                consequential_action,

            "Matched_Consequence_Terms":
                consequence["Matched_Consequence_Terms"],

            "Allowed_Before_Approval": [
                "Review machine context",
                "Review telematics alert",
                "Review service history",
                "Retrieve technical knowledge",
                "Prepare inspection plan",
                "Prepare technician requirement",
                "Prepare parts/tools checklist",
                "Prepare draft work order"
            ],

            "Not_Allowed_Before_Approval": [
                "Release consequential service action",
                "Authorize major component replacement",
                "Approve high-cost repair",
                "Confirm unverified root cause",
                "Release safety-critical repair instruction",
                "Automatically close the case"
            ]
        }

    # --------------------------------------------------------
    # RULE 2:
    # NON-CRITICAL BUT CONSEQUENTIAL ACTION -> HITL REQUIRED
    # --------------------------------------------------------

    elif consequential_action:

        return {
            "Approval_Required": True,
            "HITL_Required": True,

            "Approval_Status":
                "WAITING FOR HUMAN APPROVAL",

            "Governance_Reason":
                "Alert is non-critical, but the proposed action "
                "is consequential or safety-critical and therefore "
                "requires authorized human approval.",

            "Consequential_Action": True,

            "Matched_Consequence_Terms":
                consequence["Matched_Consequence_Terms"],

            "Allowed_Before_Approval": [
                "Review machine context",
                "Review telematics alert",
                "Review service history",
                "Retrieve technical knowledge",
                "Prepare inspection plan",
                "Prepare technician requirement",
                "Prepare parts/tools checklist",
                "Prepare draft work order"
            ],

            "Not_Allowed_Before_Approval": [
                "Release consequential service action",
                "Authorize major component replacement",
                "Approve high-cost repair",
                "Confirm unverified root cause",
                "Release safety-critical repair instruction",
                "Automatically close the case"
            ]
        }

    # --------------------------------------------------------
    # RULE 3:
    # NON-CRITICAL ROUTINE ACTION -> NO HITL
    # --------------------------------------------------------

    else:

        return {
            "Approval_Required": False,
            "HITL_Required": False,

            "Approval_Status":
                "AUTO_AUTHORIZED WITHIN APPROVED GUARDRAILS",

            "Governance_Reason":
                "Non-critical routine service action is within "
                "the approved agent guardrails. Manual HITL "
                "approval is not required.",

            "Consequential_Action": False,

            "Matched_Consequence_Terms": [],

            "Allowed_Before_Approval": [
                "Review machine context",
                "Review telematics alert",
                "Review service history",
                "Retrieve approved technical knowledge",
                "Prepare routine inspection",
                "Prepare monitoring action",
                "Prepare technician requirement",
                "Prepare parts/tools checklist",
                "Release routine simulated work order"
            ],

            "Not_Allowed_Before_Approval": [
                "Authorize major component replacement",
                "Approve high-cost repair",
                "Confirm unverified root cause",
                "Release safety-critical repair instruction",
                "Automatically close the case without outcome validation"
            ]
        }


# ============================================================
# 7. CREATE DRAFT WORK ORDER
# ============================================================

def create_draft_work_order(
    machine_serial_no,
    diagnostic_result,
    priority,
    technician,
    preparation,
    approval_gate
):

    timestamp = datetime.now()

    work_order_id = (
        "DRAFT-WO-"
        + timestamp.strftime("%Y%m%d%H%M%S")
    )

    machine_context = diagnostic_result.get(
        "Machine_Context",
        {}
    )

    alert = diagnostic_result.get(
        "Alert_Assessment",
        {}
    )

    if approval_gate["Approval_Required"]:

        release_status = (
            "BLOCKED PENDING HUMAN APPROVAL"
        )

    else:

        release_status = (
            "AUTO-AUTHORIZED FOR ROUTINE EXECUTION"
        )

    return {
        "Work_Order_ID":
            work_order_id,

        "Status":
            "DRAFT - NOT RELEASED",

        "Machine_Serial_No":
            machine_serial_no,

        "Machine_Model":
            machine_context.get(
                "Model",
                "Unknown"
            ),

        "Customer":
            machine_context.get(
                "Customer_Name",
                "Unknown"
            ),

        "Site":
            machine_context.get(
                "Site_Name",
                "Unknown"
            ),

        "City":
            machine_context.get(
                "City",
                "Unknown"
            ),

        "Current_HMR":
            machine_context.get(
                "Current_HMR",
                "Unknown"
            ),

        "Alert_Category":
            alert.get(
                "Alert_Category",
                "Unknown"
            ),

        "Alert_Severity":
            alert.get(
                "Severity",
                diagnostic_result.get(
                    "Risk_Level",
                    "Unknown"
                )
            ),

        "Priority":
            (
                priority["Priority_Code"]
                + " - "
                + priority["Priority"]
            ),

        "Inspection_Focus":
            preparation[
                "Inspection_Focus"
            ],

        "Technician_Skill":
            technician[
                "Skill_Level"
            ],

        "Technician_Profile":
            technician[
                "Technician_Profile"
            ],

        "Created_At":
            timestamp.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "HITL_Required":
            approval_gate[
                "HITL_Required"
            ],

        "Release_Status":
            release_status
    }


# ============================================================
# 8. AGENT DECISION
# ============================================================

def determine_agent_decision(approval_gate):

    if approval_gate[
        "Approval_Required"
    ]:

        return {
            "Agent_State":
                "WAITING_FOR_APPROVAL",

            "Decision":
                "Service plan prepared. Execution is blocked "
                "until authorized human approval is received.",

            "Next_Action":
                "Technical reviewer to Approve, Modify, "
                "Reject, or Escalate the proposed plan."
        }

    else:

        return {
            "Agent_State":
                "AUTO_AUTHORIZED",

            "Decision":
                "Non-critical routine service plan is within "
                "approved agent guardrails.",

            "Next_Action":
                "Proceed to simulated routine work-order "
                "execution without manual HITL approval."
        }


# ============================================================
# 9. MAIN SERVICE ORCHESTRATOR
# ============================================================

def generate_service_action_plan(machine_serial_no):

    # --------------------------------------------------------
    # STEP 14 OUTPUT
    # --------------------------------------------------------

    diagnostic = generate_diagnostic_reasoning(
        machine_serial_no
    )

    # --------------------------------------------------------
    # SERVICE PRIORITY
    # --------------------------------------------------------

    priority = determine_service_priority(
        diagnostic["Risk_Level"]
    )

    # --------------------------------------------------------
    # TECHNICIAN REQUIREMENT
    # --------------------------------------------------------

    technician = determine_technician_skill(
        diagnostic["Risk_Level"],
        diagnostic["Knowledge_Search"]
    )

    # --------------------------------------------------------
    # TOOLS / PARTS PREPARATION
    # --------------------------------------------------------

    preparation = determine_required_preparation(
        diagnostic["Knowledge_Search"]
    )

    # --------------------------------------------------------
    # CUSTOMER / SITE COORDINATION
    # --------------------------------------------------------

    coordination = determine_site_coordination(
        diagnostic["Risk_Level"]
    )

    # --------------------------------------------------------
    # RISK-BASED HITL APPROVAL GATE
    # --------------------------------------------------------

    approval = determine_approval_gate(
        diagnostic
    )

    # --------------------------------------------------------
    # DRAFT WORK ORDER
    # --------------------------------------------------------

    work_order = create_draft_work_order(
        machine_serial_no,
        diagnostic,
        priority,
        technician,
        preparation,
        approval
    )

    # --------------------------------------------------------
    # AGENT DECISION
    # --------------------------------------------------------

    agent_decision = determine_agent_decision(
        approval
    )

    # --------------------------------------------------------
    # COMPLETE ORCHESTRATION RESULT
    # --------------------------------------------------------

    result = {
        "Machine_Serial_No":
            machine_serial_no,

        "Alert_Severity":
            diagnostic.get(
                "Alert_Assessment",
                {}
            ).get(
                "Severity",
                diagnostic.get(
                    "Risk_Level",
                    "Unknown"
                )
            ),

        "Risk_Level":
            diagnostic.get(
                "Risk_Level",
                "Unknown"
            ),

        "HITL_Required":
            approval[
                "HITL_Required"
            ],

        "Agent_State":
            agent_decision[
                "Agent_State"
            ],

        "Diagnostic_Result":
            diagnostic,

        "Service_Priority":
            priority,

        "Technician_Requirement":
            technician,

        "Service_Preparation":
            preparation,

        "Customer_Site_Coordination":
            coordination,

        "Approval_Gate":
            approval,

        "Draft_Work_Order":
            work_order,

        "Agent_Decision":
            agent_decision
    }

    return result


# ============================================================
# 10. DISPLAY MANAGEMENT-FRIENDLY SERVICE PLAN
# ============================================================

def display_service_action_plan(result):

    diagnostic = result[
        "Diagnostic_Result"
    ]

    priority = result[
        "Service_Priority"
    ]

    technician = result[
        "Technician_Requirement"
    ]

    preparation = result[
        "Service_Preparation"
    ]

    coordination = result[
        "Customer_Site_Coordination"
    ]

    approval = result[
        "Approval_Gate"
    ]

    work_order = result[
        "Draft_Work_Order"
    ]

    agent = result[
        "Agent_Decision"
    ]

    alert = diagnostic[
        "Alert_Assessment"
    ]

    print("\n")
    print("=" * 78)

    print(
        "AI CAPSTONE - INTELLIGENT SERVICE ORCHESTRATOR"
    )

    print("=" * 78)

    # --------------------------------------------------------
    # MACHINE / DIAGNOSTIC SUMMARY
    # --------------------------------------------------------

    print("\n--- MACHINE / DIAGNOSTIC SUMMARY ---")

    print(
        "Machine:",
        result["Machine_Serial_No"]
    )

    print(
        "Alert:",
        alert.get(
            "Alert_Category",
            "Unknown"
        )
    )

    print(
        "Severity:",
        alert.get(
            "Severity",
            "Unknown"
        )
    )

    print(
        "Diagnostic Risk:",
        diagnostic[
            "Risk_Level"
        ]
    )

    print(
        "Knowledge Search:",
        diagnostic[
            "Knowledge_Search"
        ]
    )

    print(
        "Diagnostic Confidence:",
        diagnostic[
            "Confidence"
        ]
    )

    # --------------------------------------------------------
    # SERVICE PRIORITY
    # --------------------------------------------------------

    print("\n--- SERVICE PRIORITY ---")

    print(
        "Priority:",
        priority["Priority_Code"],
        "-",
        priority["Priority"]
    )

    print(
        "Response Strategy:",
        priority[
            "Response_Strategy"
        ]
    )

    # --------------------------------------------------------
    # TECHNICIAN REQUIREMENT
    # --------------------------------------------------------

    print("\n--- TECHNICIAN REQUIREMENT ---")

    print(
        "Skill Level:",
        technician[
            "Skill_Level"
        ]
    )

    print(
        "Profile:",
        technician[
            "Technician_Profile"
        ]
    )

    print(
        "Reason:",
        technician[
            "Reason"
        ]
    )

    # --------------------------------------------------------
    # INSPECTION / PREPARATION
    # --------------------------------------------------------

    print("\n--- SERVICE PREPARATION ---")

    print(
        "Inspection Focus:",
        preparation[
            "Inspection_Focus"
        ]
    )

    print("\nTools / Equipment:")

    for number, item in enumerate(
        preparation[
            "Tools_Equipment"
        ],
        start=1
    ):

        print(
            f"{number}. {item}"
        )

    print("\nParts / Consumables To Check:")

    for number, item in enumerate(
        preparation[
            "Parts_Consumables_To_Check"
        ],
        start=1
    ):

        print(
            f"{number}. {item}"
        )

    # --------------------------------------------------------
    # DIAGNOSTIC ACTION
    # --------------------------------------------------------

    print("\n--- AI RECOMMENDED ACTIONS ---")

    actions = diagnostic.get(
        "Recommended_Actions",
        []
    )

    if actions:

        if isinstance(actions, str):
            actions = [actions]

        for number, action in enumerate(
            actions,
            start=1
        ):

            print(
                f"{number}. {action}"
            )

    else:

        print(
            "No automatic repair recommendation available."
        )

    # --------------------------------------------------------
    # CUSTOMER / SITE
    # --------------------------------------------------------

    print("\n--- CUSTOMER / SITE COORDINATION ---")

    print(
        "Customer Contact Required:",
        coordination[
            "Customer_Contact_Required"
        ]
    )

    print(
        "Site Coordination Required:",
        coordination[
            "Site_Coordination_Required"
        ]
    )

    print(
        "Communication:",
        coordination[
            "Recommended_Message"
        ]
    )

    # --------------------------------------------------------
    # WORK ORDER
    # --------------------------------------------------------

    print("\n--- DRAFT WORK ORDER ---")

    print(
        "Work Order ID:",
        work_order[
            "Work_Order_ID"
        ]
    )

    print(
        "Status:",
        work_order[
            "Status"
        ]
    )

    print(
        "Machine:",
        work_order[
            "Machine_Serial_No"
        ]
    )

    print(
        "Model:",
        work_order[
            "Machine_Model"
        ]
    )

    print(
        "Customer:",
        work_order[
            "Customer"
        ]
    )

    print(
        "Site:",
        work_order[
            "Site"
        ]
    )

    print(
        "City:",
        work_order[
            "City"
        ]
    )

    print(
        "HMR:",
        work_order[
            "Current_HMR"
        ]
    )

    print(
        "Priority:",
        work_order[
            "Priority"
        ]
    )

    print(
        "Inspection:",
        work_order[
            "Inspection_Focus"
        ]
    )

    print(
        "Technician:",
        work_order[
            "Technician_Profile"
        ]
    )

    print(
        "Release Status:",
        work_order[
            "Release_Status"
        ]
    )

    # --------------------------------------------------------
    # RISK-BASED HITL
    # --------------------------------------------------------

    print("\n--- RISK-BASED HUMAN-IN-THE-LOOP GATE ---")

    print(
        "Alert Severity:",
        result[
            "Alert_Severity"
        ]
    )

    print(
        "Approval Required:",
        approval[
            "Approval_Required"
        ]
    )

    print(
        "HITL Required:",
        approval[
            "HITL_Required"
        ]
    )

    print(
        "Approval Status:",
        approval[
            "Approval_Status"
        ]
    )

    print(
        "Governance Reason:",
        approval[
            "Governance_Reason"
        ]
    )

    print(
        "Consequential Action:",
        approval[
            "Consequential_Action"
        ]
    )

    if approval[
        "Matched_Consequence_Terms"
    ]:

        print(
            "Consequence Trigger:",
            ", ".join(
                approval[
                    "Matched_Consequence_Terms"
                ]
            )
        )

    if approval[
        "Approval_Required"
    ]:

        print("\nAgent CAN do before approval:")

        for item in approval[
            "Allowed_Before_Approval"
        ]:

            print(
                "-",
                item
            )

        print("\nAgent CANNOT do before approval:")

        for item in approval[
            "Not_Allowed_Before_Approval"
        ]:

            print(
                "-",
                item
            )

    else:

        print(
            "\nNo manual HITL approval is required "
            "for this routine non-critical case."
        )

        print(
            "The agent may proceed within the "
            "defined guardrails."
        )

    # --------------------------------------------------------
    # AGENT STATE
    # --------------------------------------------------------

    print("\n--- AGENTIC AI STATUS ---")

    print(
        "Agent State:",
        agent[
            "Agent_State"
        ]
    )

    print(
        "Decision:",
        agent[
            "Decision"
        ]
    )

    print(
        "Next Action:",
        agent[
            "Next_Action"
        ]
    )

    # --------------------------------------------------------
    # END
    # --------------------------------------------------------

    print("\n" + "=" * 78)

    print(
        "INTELLIGENT SERVICE ACTION PLAN COMPLETE"
    )

    if approval[
        "Approval_Required"
    ]:

        print(
            "Workflow: Predict -> Diagnose -> Plan -> "
            "Human Approve -> Execute -> Learn"
        )

        print(
            "Next: Step 16 - Human Approval + "
            "Work Order Execution Simulation"
        )

    else:

        print(
            "Workflow: Predict -> Diagnose -> Plan -> "
            "Auto-Authorize -> Execute -> Learn"
        )

        print(
            "Next: Step 16 - Automatic Routine "
            "Work Order Execution Simulation"
        )

    print("=" * 78)


# ============================================================
# 11. PROTOTYPE SHOWCASE
# ============================================================

if __name__ == "__main__":

    # Same Critical showcase machine used in earlier steps
    machine_serial = "XYZ20T100388"

    service_plan = generate_service_action_plan(
        machine_serial
    )

    display_service_action_plan(
        service_plan
    )