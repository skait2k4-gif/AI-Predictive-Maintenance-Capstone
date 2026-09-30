# ============================================================
# STEP 13 - INTEGRATED DIAGNOSTIC CONTEXT TOOL
# AI-Powered Predictive Maintenance & Intelligent Service
# Management Capstone Prototype
#
# Purpose:
# Combine all 5 data layers for one machine:
# 1. Machine Population
# 2. Service History
# 3. Telematics Alerts
# 4. Troubleshooting Manual
# 5. Operation & Maintenance Manual
# ============================================================


# ------------------------------------------------------------
# IMPORT OUR EXISTING TOOLS
# ------------------------------------------------------------

from machine_tool import get_machine_details
from service_history_tool import get_service_history
from telematics_tool import get_machine_alerts
from troubleshooting_tool import search_troubleshooting
from om_manual_tool import search_om_manual


# ============================================================
# BUILD INTEGRATED DIAGNOSTIC CONTEXT
# ============================================================

def build_diagnostic_context(machine_serial_no):

    print("\n" + "=" * 75)
    print("AI CAPSTONE - INTEGRATED DIAGNOSTIC CONTEXT")
    print("=" * 75)

    # --------------------------------------------------------
    # LAYER 1 - MACHINE POPULATION
    # --------------------------------------------------------

    machine = get_machine_details(machine_serial_no)


    # --------------------------------------------------------
    # LAYER 2 - SERVICE HISTORY
    # --------------------------------------------------------

    service_history = get_service_history(machine_serial_no)


    # --------------------------------------------------------
    # LAYER 3 - TELEMATICS ALERTS
    # --------------------------------------------------------

    alerts = get_machine_alerts(machine_serial_no)


    # --------------------------------------------------------
    # PREPARE KNOWLEDGE RETRIEVAL
    # --------------------------------------------------------

    troubleshooting = []
    om_guidance = []
    search_text = ""


    # --------------------------------------------------------
    # IDENTIFY LATEST ALERT AND CREATE SEARCH KEYWORD
    # --------------------------------------------------------

    if not isinstance(alerts, str) and len(alerts) > 0:

        latest_alert = alerts[0]

        alert_category = str(
            latest_alert.get("Alert_Category", "")
        )

        alert_description = str(
            latest_alert.get("Alert_Description", "")
        )

        parameter_name = str(
            latest_alert.get("Parameter_Name", "")
        )

        # Combine alert information
        alert_text = (
            alert_category
            + " "
            + alert_description
            + " "
            + parameter_name
        ).lower()


        # ----------------------------------------------------
        # CONVERT ALERT INTO SIMPLE KNOWLEDGE SEARCH KEYWORD
        # ----------------------------------------------------

        if (
            "cooling" in alert_text
            or "coolant" in alert_text
            or "temperature" in alert_text
            or "temp" in alert_text
        ):
            search_text = "cooling"

        elif (
            "air" in alert_text
            or "filter" in alert_text
            or "intake" in alert_text
        ):
            search_text = "air"

        elif "hydraulic" in alert_text:
            search_text = "hydraulic"

        elif (
            "electrical" in alert_text
            or "voltage" in alert_text
            or "battery" in alert_text
        ):
            search_text = "electrical"

        else:
            search_text = alert_category


        print("\nKnowledge Search Keyword:", search_text)


        # ----------------------------------------------------
        # LAYER 4 - TROUBLESHOOTING MANUAL
        # ----------------------------------------------------

        troubleshooting = search_troubleshooting(
            search_text
        )


        # ----------------------------------------------------
        # LAYER 5 - OPERATION & MAINTENANCE MANUAL
        # ----------------------------------------------------

        om_guidance = search_om_manual(
            search_text
        )


    # --------------------------------------------------------
    # BUILD ONE INTEGRATED MACHINE CONTEXT
    # --------------------------------------------------------

    diagnostic_context = {

        "Machine_Serial_No":
            machine_serial_no,

        "Machine_Details":
            machine,

        "Service_History":
            service_history,

        "Telematics_Alerts":
            alerts,

        "Knowledge_Search_Keyword":
            search_text,

        "Troubleshooting_Guidance":
            troubleshooting,

        "OM_Guidance":
            om_guidance
    }


    return diagnostic_context


# ============================================================
# TEST THE TOOL USING OUR SHOWCASE MACHINE
# ============================================================

machine_serial = "XYZ20T100388"

context = build_diagnostic_context(
    machine_serial
)


# ============================================================
# DISPLAY RESULTS
# ============================================================


# ------------------------------------------------------------
# MACHINE DETAILS
# ------------------------------------------------------------

print("\n")
print("=" * 75)
print("1. MACHINE DETAILS")
print("=" * 75)

print(
    context["Machine_Details"]
)


# ------------------------------------------------------------
# TELEMATICS ALERT
# ------------------------------------------------------------

print("\n")
print("=" * 75)
print("2. LATEST TELEMATICS ALERT")
print("=" * 75)

if isinstance(
    context["Telematics_Alerts"],
    str
):
    print(
        context["Telematics_Alerts"]
    )

else:

    if len(
        context["Telematics_Alerts"]
    ) > 0:

        latest_alert = (
            context["Telematics_Alerts"][0]
        )

        print(
            latest_alert
        )

    else:
        print(
            "No telematics alerts found."
        )


# ------------------------------------------------------------
# SERVICE HISTORY
# ------------------------------------------------------------

print("\n")
print("=" * 75)
print("3. RECENT SERVICE HISTORY")
print("=" * 75)

if isinstance(
    context["Service_History"],
    str
):
    print(
        context["Service_History"]
    )

else:

    print(
        "Total Service Records:",
        len(context["Service_History"])
    )

    print(
        "\nLatest 5 Service Records:"
    )

    for record in (
        context["Service_History"][-5:]
    ):

        print(
            "\n",
            record
        )


# ------------------------------------------------------------
# KNOWLEDGE SEARCH
# ------------------------------------------------------------

print("\n")
print("=" * 75)
print("4. KNOWLEDGE SEARCH")
print("=" * 75)

print(
    "Search Keyword:",
    context["Knowledge_Search_Keyword"]
)


# ------------------------------------------------------------
# TROUBLESHOOTING MANUAL
# ------------------------------------------------------------

print("\n")
print("=" * 75)
print("5. TROUBLESHOOTING KNOWLEDGE")
print("=" * 75)

troubleshooting_results = (
    context["Troubleshooting_Guidance"]
)

if isinstance(
    troubleshooting_results,
    str
):
    print(
        troubleshooting_results
    )

elif len(
    troubleshooting_results
) == 0:

    print(
        "No troubleshooting guidance found."
    )

else:

    print(
        "Relevant Troubleshooting Records:",
        len(troubleshooting_results)
    )

    for item in (
        troubleshooting_results[:3]
    ):

        print(
            "\n------------------------------"
        )

        print(
            "Document:",
            item.get(
                "Doc_ID",
                ""
            )
        )

        print(
            "Section:",
            item.get(
                "Section_ID",
                ""
            )
        )

        print(
            "System:",
            item.get(
                "System",
                ""
            )
        )

        print(
            "Symptom / Alert:",
            item.get(
                "Symptom_or_Alert",
                ""
            )
        )

        print(
            "Possible Cause:",
            item.get(
                "Possible_Cause",
                ""
            )
        )

        print(
            "Inspection:",
            item.get(
                "Inspection_Sequence",
                ""
            )
        )

        print(
            "Recommended Action:",
            item.get(
                "Recommended_Action",
                ""
            )
        )

        print(
            "Escalation:",
            item.get(
                "Escalation_Criteria",
                ""
            )
        )

        print(
            "Safety / HITL:",
            item.get(
                "Safety_HITL_Note",
                ""
            )
        )


# ------------------------------------------------------------
# OPERATION & MAINTENANCE MANUAL
# ------------------------------------------------------------

print("\n")
print("=" * 75)
print("6. O&M KNOWLEDGE")
print("=" * 75)

om_results = (
    context["OM_Guidance"]
)

if isinstance(
    om_results,
    str
):
    print(
        om_results
    )

elif len(
    om_results
) == 0:

    print(
        "No O&M guidance found."
    )

else:

    print(
        "Relevant O&M Records:",
        len(om_results)
    )

    for item in (
        om_results[:3]
    ):

        print(
            "\n------------------------------"
        )

        print(
            "Document:",
            item.get(
                "Doc_ID",
                ""
            )
        )

        print(
            "Section:",
            item.get(
                "Section_ID",
                ""
            )
        )

        print(
            "Topic:",
            item.get(
                "Topic",
                ""
            )
        )

        print(
            "Guidance:",
            item.get(
                "Operating_or_Maintenance_Guidance",
                ""
            )
        )

        print(
            "Inspection / Action:",
            item.get(
                "Inspection_or_Action",
                ""
            )
        )

        print(
            "Interval / Trigger:",
            item.get(
                "Interval_or_Trigger",
                ""
            )
        )

        print(
            "Warning / Limitation:",
            item.get(
                "Warning_or_Limitation",
                ""
            )
        )


# ============================================================
# FINAL STATUS
# ============================================================

print("\n")
print("=" * 75)
print("INTEGRATED DIAGNOSTIC CONTEXT READY")
print("=" * 75)

print(
    "\nMachine:",
    machine_serial
)

print(
    "Knowledge Search:",
    context["Knowledge_Search_Keyword"]
)

print(
    "\n5-Layer Integration:"
)

print(
    "1. Machine Population       : CONNECTED"
)

print(
    "2. Service History          : CONNECTED"
)

print(
    "3. Telematics Alerts        : CONNECTED"
)

print(
    "4. Troubleshooting Manual   : CONNECTED"
)

print(
    "5. O&M Manual               : CONNECTED"
)

print(
    "\nReady for Step 14 - AI Diagnostic Reasoning"
)

print(
    "=" * 75
)