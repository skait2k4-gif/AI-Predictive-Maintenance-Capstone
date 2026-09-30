# ============================================================
# STEP 14 - AI DIAGNOSTIC REASONING ENGINE
# Group 16 Capstone:
# AI-Powered Predictive Maintenance &
# Intelligent Service Management
# ============================================================

from machine_tool import get_machine_details
from service_history_tool import get_service_history
from telematics_tool import get_machine_alerts
from troubleshooting_tool import search_troubleshooting
from om_manual_tool import search_om_manual


# ------------------------------------------------------------
# 1. Helper function
# ------------------------------------------------------------

def safe_list(value):
    """Convert tool output into a safe list."""
    if isinstance(value, list):
        return value

    return []


# ------------------------------------------------------------
# 2. Determine knowledge-search topic from telematics alert
# ------------------------------------------------------------

def determine_search_topic(alerts):

    if not alerts:
        return "general"

    latest_alert = alerts[0]

    category = str(
        latest_alert.get("Alert_Category", "")
    ).lower()

    description = str(
        latest_alert.get("Alert_Description", "")
    ).lower()

    parameter = str(
        latest_alert.get("Parameter_Name", "")
    ).lower()

    combined_text = f"{category} {description} {parameter}"

    if any(
        word in combined_text
        for word in [
            "cooling",
            "coolant",
            "temperature",
            "overheat"
        ]
    ):
        return "cooling"

    if any(
        word in combined_text
        for word in [
            "air intake",
            "air filter",
            "restriction"
        ]
    ):
        return "air"

    if any(
        word in combined_text
        for word in [
            "hydraulic",
            "hydraulic temperature"
        ]
    ):
        return "hydraulic"

    if any(
        word in combined_text
        for word in [
            "electrical",
            "voltage",
            "battery"
        ]
    ):
        return "electrical"

    return "general"


# ------------------------------------------------------------
# 3. Determine diagnostic risk level
# ------------------------------------------------------------

def determine_risk_level(alerts):

    if not alerts:
        return "LOW"

    severity_values = [
        str(alert.get("Severity", "")).lower()
        for alert in alerts
    ]

    if "critical" in severity_values:
        return "CRITICAL"

    if "high" in severity_values:
        return "HIGH"

    if "medium" in severity_values:
        return "MEDIUM"

    return "LOW"


# ------------------------------------------------------------
# 4. Extract important service-history observations
# ------------------------------------------------------------

def analyse_service_history(history, search_topic):

    if not history:
        return {
            "Total_Service_Records": 0,
            "Relevant_History_Count": 0,
            "Observation":
                "No service history available."
        }

    keywords = {
        "cooling": [
            "cool",
            "coolant",
            "radiator",
            "temperature",
            "overheat",
            "hose",
            "belt"
        ],

        "air": [
            "air",
            "filter",
            "restriction",
            "intake"
        ],

        "hydraulic": [
            "hydraulic",
            "oil",
            "pressure",
            "temperature"
        ],

        "electrical": [
            "electrical",
            "battery",
            "voltage",
            "wiring",
            "sensor"
        ]
    }

    search_words = keywords.get(
        search_topic,
        [search_topic]
    )

    relevant_records = []

    for record in history:

        record_text = " ".join(
            str(value).lower()
            for value in record.values()
        )

        if any(
            word in record_text
            for word in search_words
        ):
            relevant_records.append(record)

    if relevant_records:

        observation = (
            f"{len(relevant_records)} historical service "
            f"records contain information relevant to "
            f"{search_topic}."
        )

    else:

        observation = (
            f"No directly related {search_topic} repair "
            "was identified in the available service history."
        )

    return {
        "Total_Service_Records": len(history),
        "Relevant_History_Count": len(relevant_records),
        "Observation": observation
    }


# ------------------------------------------------------------
# 5. Build evidence from troubleshooting manual
# ------------------------------------------------------------

def build_troubleshooting_evidence(records):

    evidence = []

    for item in records[:5]:

        evidence.append({

            "Document":
                item.get("Doc_ID"),

            "Section":
                item.get("Section_ID"),

            "Symptom":
                item.get("Symptom_or_Alert"),

            "Possible_Cause":
                item.get("Possible_Cause"),

            "Inspection":
                item.get("Inspection_Sequence"),

            "Recommended_Action":
                item.get("Recommended_Action"),

            "Escalation":
                item.get("Escalation_Criteria"),

            "Safety_HITL":
                item.get("Safety_HITL_Note")
        })

    return evidence


# ------------------------------------------------------------
# 6. Build evidence from O&M manual
# ------------------------------------------------------------

def build_om_evidence(records):

    evidence = []

    for item in records[:5]:

        evidence.append({

            "Document":
                item.get("Doc_ID"),

            "Section":
                item.get("Section_ID"),

            "Topic":
                item.get("Topic"),

            "Guidance":
                item.get(
                    "Operating_or_Maintenance_Guidance"
                ),

            "Inspection_Action":
                item.get(
                    "Inspection_or_Action"
                ),

            "Interval_Trigger":
                item.get(
                    "Interval_or_Trigger"
                ),

            "Warning_Limitation":
                item.get(
                    "Warning_or_Limitation"
                )
        })

    return evidence


# ------------------------------------------------------------
# 7. Main AI diagnostic reasoning function
# ------------------------------------------------------------

def generate_diagnostic_reasoning(machine_serial_no):

    # --------------------------------------------------------
    # Retrieve Layer 1 - Machine Population
    # --------------------------------------------------------

    machine = get_machine_details(
        machine_serial_no
    )

    # --------------------------------------------------------
    # Retrieve Layer 2 - Service History
    # --------------------------------------------------------

    history_raw = get_service_history(
        machine_serial_no
    )

    history = safe_list(history_raw)

    # --------------------------------------------------------
    # Retrieve Layer 3 - Telematics
    # --------------------------------------------------------

    alerts_raw = get_machine_alerts(
        machine_serial_no
    )

    alerts = safe_list(alerts_raw)

    # --------------------------------------------------------
    # Determine search topic
    # --------------------------------------------------------

    search_topic = determine_search_topic(
        alerts
    )

    # --------------------------------------------------------
    # Retrieve Layer 4 - Troubleshooting Manual
    # --------------------------------------------------------

    troubleshooting_raw = (
        search_troubleshooting(
            search_topic
        )
    )

    troubleshooting = safe_list(
        troubleshooting_raw
    )

    # --------------------------------------------------------
    # Retrieve Layer 5 - O&M Manual
    # --------------------------------------------------------

    om_raw = search_om_manual(
        search_topic
    )

    om_records = safe_list(
        om_raw
    )

    # --------------------------------------------------------
    # Diagnostic Risk Assessment
    # --------------------------------------------------------

    risk_level = determine_risk_level(
        alerts
    )

    # --------------------------------------------------------
    # Service History Analysis
    # --------------------------------------------------------

    history_analysis = (
        analyse_service_history(
            history,
            search_topic
        )
    )

    # --------------------------------------------------------
    # Knowledge Evidence
    # --------------------------------------------------------

    troubleshooting_evidence = (
        build_troubleshooting_evidence(
            troubleshooting
        )
    )

    om_evidence = build_om_evidence(
        om_records
    )

    # --------------------------------------------------------
    # Latest Alert
    # --------------------------------------------------------

    latest_alert = (
        alerts[0]
        if alerts
        else {}
    )

    # --------------------------------------------------------
    # Diagnostic Summary
    # --------------------------------------------------------

    alert_category = latest_alert.get(
        "Alert_Category",
        "No active alert"
    )

    severity = latest_alert.get(
        "Severity",
        "Unknown"
    )

    parameter = latest_alert.get(
        "Parameter_Name",
        "Unknown"
    )

    parameter_value = latest_alert.get(
        "Parameter_Value",
        "Unknown"
    )

    if troubleshooting_evidence:

        probable_causes = [
            item["Possible_Cause"]
            for item
            in troubleshooting_evidence
            if item.get("Possible_Cause")
        ]

        inspections = [
            item["Inspection"]
            for item
            in troubleshooting_evidence
            if item.get("Inspection")
        ]

        recommended_actions = [
            item["Recommended_Action"]
            for item
            in troubleshooting_evidence
            if item.get("Recommended_Action")
        ]

    else:

        probable_causes = [
            "Insufficient approved troubleshooting "
            "evidence available."
        ]

        inspections = [
            "Escalate for technical investigation."
        ]

        recommended_actions = [
            "Human technical review required."
        ]

    # --------------------------------------------------------
    # Human approval logic
    # --------------------------------------------------------

    if risk_level in [
        "CRITICAL",
        "HIGH"
    ]:

        hitl_required = True

        hitl_message = (
            "Human technical approval required before "
            "major repair, component replacement, "
            "machine shutdown decision, or other "
            "consequential service action."
        )

    else:

        hitl_required = False

        hitl_message = (
            "AI recommendation may support inspection, "
            "but technician validation remains required."
        )

    # --------------------------------------------------------
    # Confidence logic
    # --------------------------------------------------------

    evidence_score = 0

    if alerts:
        evidence_score += 1

    if history:
        evidence_score += 1

    if troubleshooting_evidence:
        evidence_score += 1

    if om_evidence:
        evidence_score += 1

    if evidence_score == 4:
        confidence = "HIGH"

    elif evidence_score >= 2:
        confidence = "MEDIUM"

    else:
        confidence = "LOW"

    # --------------------------------------------------------
    # Final Diagnostic Object
    # --------------------------------------------------------

    diagnostic_result = {

        "Machine_Serial_No":
            machine_serial_no,

        "Machine_Context":
            machine,

        "Knowledge_Search":
            search_topic,

        "Risk_Level":
            risk_level,

        "Alert_Assessment": {

            "Alert_Category":
                alert_category,

            "Severity":
                severity,

            "Parameter":
                parameter,

            "Parameter_Value":
                parameter_value
        },

        "Service_History_Assessment":
            history_analysis,

        "Probable_Causes":
            probable_causes,

        "Recommended_Inspection_Sequence":
            inspections,

        "Recommended_Actions":
            recommended_actions,

        "Troubleshooting_Evidence":
            troubleshooting_evidence,

        "OM_Evidence":
            om_evidence,

        "Confidence":
            confidence,

        "HITL_Required":
            hitl_required,

        "HITL_Message":
            hitl_message
    }

    return diagnostic_result


# ============================================================
# 8. PRESENTATION / DEMO OUTPUT
# ============================================================

def display_diagnostic_report(result):

    print("\n")
    print("=" * 78)
    print("AI CAPSTONE - AI DIAGNOSTIC REASONING ENGINE")
    print("=" * 78)

    print(
        "\nMachine:",
        result["Machine_Serial_No"]
    )

    print(
        "Knowledge Search:",
        result["Knowledge_Search"]
    )

    print(
        "Diagnostic Risk:",
        result["Risk_Level"]
    )

    print(
        "Confidence:",
        result["Confidence"]
    )

    # --------------------------------------------------------
    # Alert
    # --------------------------------------------------------

    print("\n--- CURRENT MACHINE CONDITION ---")

    alert = result["Alert_Assessment"]

    print(
        "Alert Category:",
        alert["Alert_Category"]
    )

    print(
        "Severity:",
        alert["Severity"]
    )

    print(
        "Parameter:",
        alert["Parameter"]
    )

    print(
        "Parameter Value:",
        alert["Parameter_Value"]
    )

    # --------------------------------------------------------
    # Service history
    # --------------------------------------------------------

    print("\n--- SERVICE HISTORY INTELLIGENCE ---")

    history = result[
        "Service_History_Assessment"
    ]

    print(
        "Total Service Records:",
        history["Total_Service_Records"]
    )

    print(
        "Relevant Historical Records:",
        history["Relevant_History_Count"]
    )

    print(
        "Observation:",
        history["Observation"]
    )

    # --------------------------------------------------------
    # Probable causes
    # --------------------------------------------------------

    print("\n--- AI PROBABLE CAUSES ---")

    for number, cause in enumerate(
        result["Probable_Causes"],
        start=1
    ):

        print(
            f"{number}. {cause}"
        )

    # --------------------------------------------------------
    # Inspection
    # --------------------------------------------------------

    print("\n--- RECOMMENDED INSPECTION ---")

    for number, inspection in enumerate(
        result[
            "Recommended_Inspection_Sequence"
        ],
        start=1
    ):

        print(
            f"{number}. {inspection}"
        )

    # --------------------------------------------------------
    # Recommended actions
    # --------------------------------------------------------

    print("\n--- RECOMMENDED SERVICE ACTION ---")

    for number, action in enumerate(
        result["Recommended_Actions"],
        start=1
    ):

        print(
            f"{number}. {action}"
        )

    # --------------------------------------------------------
    # Troubleshooting evidence
    # --------------------------------------------------------

    print("\n--- TROUBLESHOOTING EVIDENCE ---")

    if result["Troubleshooting_Evidence"]:

        for item in result[
            "Troubleshooting_Evidence"
        ]:

            print(
                "\nSource:",
                item["Document"],
                "/",
                item["Section"]
            )

            print(
                "Possible Cause:",
                item["Possible_Cause"]
            )

    else:

        print(
            "No approved troubleshooting evidence retrieved."
        )

    # --------------------------------------------------------
    # O&M evidence
    # --------------------------------------------------------

    print("\n--- O&M MANUAL EVIDENCE ---")

    if result["OM_Evidence"]:

        for item in result["OM_Evidence"]:

            print(
                "\nSource:",
                item["Document"],
                "/",
                item["Section"]
            )

            print(
                "Topic:",
                item["Topic"]
            )

            print(
                "Guidance:",
                item["Guidance"]
            )

    else:

        print(
            "No approved O&M evidence retrieved."
        )

    # --------------------------------------------------------
    # HITL
    # --------------------------------------------------------

    print("\n--- HUMAN-IN-THE-LOOP CONTROL ---")

    print(
        "Human Approval Required:",
        result["HITL_Required"]
    )

    print(
        "Control:",
        result["HITL_Message"]
    )

    print("\n" + "=" * 78)

    print(
        "AI DIAGNOSTIC REASONING COMPLETE"
    )

    print(
        "Next: Step 15 - Intelligent Service "
        "Action Planning / Agentic Orchestration"
    )

    print("=" * 78)


# ============================================================
# 9. TEST / PROTOTYPE SHOWCASE
# ============================================================

if __name__ == "__main__":

    # Current showcase machine from Step 13
    machine_serial = "XYZ20T100388"

    result = generate_diagnostic_reasoning(
        machine_serial
    )

    display_diagnostic_report(
        result
    )