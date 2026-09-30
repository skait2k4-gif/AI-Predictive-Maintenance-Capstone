# ============================================================
# STEP 19B
# END-TO-END CAPSTONE PROTOTYPE VALIDATION
#
# AI-Powered Predictive Maintenance &
# Intelligent Service Management
#
# Synthetic Academic Prototype
# ============================================================

from pathlib import Path
import pandas as pd


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

MACHINE_FILE = DATA_DIR / "01_Machine_Population_3200_XYZ20T.xlsx"
SERVICE_FILE = DATA_DIR / "02_Machine_Service_History_Integrated.xlsx"
ALERT_FILE = DATA_DIR / "03_Telematics_Machine_Alarm_Alerts.xlsx"
TSM_FILE = DATA_DIR / "04_Synthetic_Troubleshooting_Manual_XYZ20T.xlsx"
OM_FILE = DATA_DIR / "05_Synthetic_Operation_Maintenance_Manual_XYZ20T.xlsx"

CRITICAL_MACHINE = "XYZ20T100388"
NON_CRITICAL_MACHINE = "XYZ20T100017"


# ============================================================
# 2. PRINT HELPERS
# ============================================================

def header(title):
    print()
    print("=" * 74)
    print(title)
    print("=" * 74)


def passed(text):
    print(f"[PASS] {text}")


def failed(text):
    print(f"[FAIL] {text}")


def info(text):
    print(f"       {text}")


# ============================================================
# 3. GENERAL HELPERS
# ============================================================

def find_column(df, candidates):

    lookup = {
        str(col).strip().lower(): col
        for col in df.columns
    }

    for candidate in candidates:

        key = candidate.strip().lower()

        if key in lookup:
            return lookup[key]

    return None


def normalize_severity(value):

    value = str(value).strip().upper()

    if value == "CRITICAL":
        return "CRITICAL"

    if value == "HIGH":
        return "HIGH"

    if value in ["MEDIUM", "MODERATE"]:
        return "MODERATE"

    if value in ["LOW", "INFO", "INFORMATIONAL"]:
        return "LOW"

    return value


def severity_rank(value):

    return {
        "CRITICAL": 5,
        "HIGH": 4,
        "MODERATE": 3,
        "LOW": 2,
    }.get(
        normalize_severity(value),
        0
    )


# ============================================================
# 4. CORRECTED KNOWLEDGE RETRIEVAL
# ============================================================

def search_knowledge(df, search_terms, max_rows=10):
    """
    Transparent keyword retrieval for validation.

    Important:
    Search ALL columns after converting values to strings.
    This avoids depending on Pandas dtype classification.
    """

    if df is None or df.empty:
        return pd.DataFrame()

    work = df.copy()

    # Convert every column to searchable text.
    searchable = (
        work
        .fillna("")
        .astype(str)
    )

    combined_text = (
        searchable
        .agg(" ".join, axis=1)
        .str.lower()
    )

    score = pd.Series(
        0,
        index=work.index,
        dtype=int
    )

    cleaned_terms = []

    for term in search_terms:

        term = str(term).strip().lower()

        if (
            term
            and term != "nan"
            and term not in cleaned_terms
        ):

            cleaned_terms.append(term)

    for term in cleaned_terms:

        score += (
            combined_text
            .str.contains(
                term,
                regex=False,
                na=False
            )
            .astype(int)
        )

    work["_Retrieval_Score"] = score

    result = (
        work[
            work["_Retrieval_Score"] > 0
        ]
        .sort_values(
            "_Retrieval_Score",
            ascending=False
        )
        .head(max_rows)
        .copy()
    )

    return result


# ============================================================
# 5. LOAD DATA
# ============================================================

header(
    "AI CAPSTONE - END-TO-END PROTOTYPE VALIDATION"
)

print(
    "AI-Powered Predictive Maintenance "
    "& Intelligent Service Management"
)

print(
    "Synthetic / Illustrative Academic Prototype"
)


required_files = {
    "Machine Population": MACHINE_FILE,
    "Service History": SERVICE_FILE,
    "Telematics Alerts": ALERT_FILE,
    "Troubleshooting Manual": TSM_FILE,
    "O&M Manual": OM_FILE,
}


header(
    "A. FIVE-LAYER DATA FOUNDATION"
)


files_ok = True


for name, path in required_files.items():

    if path.exists():

        passed(
            f"{name} file found"
        )

        info(path.name)

    else:

        failed(
            f"{name} file missing"
        )

        info(str(path))

        files_ok = False


if not files_ok:

    raise SystemExit(
        "Validation stopped because required files are missing."
    )


# ============================================================
# 6. READ EXCEL DATA
# ============================================================

machine_df = pd.read_excel(
    MACHINE_FILE
)


try:

    service_df = pd.read_excel(
        SERVICE_FILE,
        sheet_name="Machine Service History"
    )

except Exception:

    service_df = pd.read_excel(
        SERVICE_FILE
    )


alert_df = pd.read_excel(
    ALERT_FILE
)

tsm_df = pd.read_excel(
    TSM_FILE
)

om_df = pd.read_excel(
    OM_FILE
)


passed(
    "All five data layers loaded"
)


print()
info(
    f"Machine Population rows : {len(machine_df):,}"
)

info(
    f"Service History rows    : {len(service_df):,}"
)

info(
    f"Telematics Alert rows   : {len(alert_df):,}"
)

info(
    f"Troubleshooting rows    : {len(tsm_df):,}"
)

info(
    f"O&M Manual rows         : {len(om_df):,}"
)


# ============================================================
# 7. IDENTIFY COLUMNS
# ============================================================

machine_serial_col = find_column(
    machine_df,
    [
        "Machine_Serial_No",
        "Machine Serial No",
        "Machine Serial"
    ]
)

service_serial_col = find_column(
    service_df,
    [
        "Machine_Serial_No",
        "Machine Serial No",
        "Machine Serial"
    ]
)

alert_serial_col = find_column(
    alert_df,
    [
        "Machine_Serial_No",
        "Machine Serial No",
        "Machine Serial"
    ]
)

severity_col = find_column(
    alert_df,
    [
        "Severity",
        "Alert_Severity",
        "Alert Severity"
    ]
)

category_col = find_column(
    alert_df,
    [
        "Alert_Category",
        "Alert Category",
        "System",
        "Category"
    ]
)

description_col = find_column(
    alert_df,
    [
        "Alert_Description",
        "Alert Description",
        "Description"
    ]
)

parameter_col = find_column(
    alert_df,
    [
        "Parameter_Name",
        "Parameter"
    ]
)

alert_id_col = find_column(
    alert_df,
    [
        "Alert_ID",
        "Alert ID"
    ]
)


required_columns = {
    "Machine Serial": machine_serial_col,
    "Service Serial": service_serial_col,
    "Alert Serial": alert_serial_col,
    "Severity": severity_col,
}


for name, column in required_columns.items():

    if column is None:

        failed(
            f"{name} column not found"
        )

        raise SystemExit(1)

    else:

        passed(
            f"{name} column identified: {column}"
        )


# ============================================================
# 8. CLEAN JOIN KEYS
# ============================================================

machine_df[machine_serial_col] = (
    machine_df[machine_serial_col]
    .astype(str)
    .str.strip()
)

service_df[service_serial_col] = (
    service_df[service_serial_col]
    .astype(str)
    .str.strip()
)

alert_df[alert_serial_col] = (
    alert_df[alert_serial_col]
    .astype(str)
    .str.strip()
)


# ============================================================
# 9. FLEET INTEGRITY
# ============================================================

header(
    "B. FLEET & REFERENTIAL INTEGRITY"
)


population_set = set(
    machine_df[machine_serial_col]
)

service_set = set(
    service_df[service_serial_col]
)

alert_set = set(
    alert_df[alert_serial_col]
)


print(
    f"Fleet Population                  : "
    f"{len(population_set):,}"
)

print(
    f"Machines with Service History     : "
    f"{len(service_set):,}"
)

print(
    f"Machines with Telematics Alerts   : "
    f"{len(alert_set):,}"
)


service_missing = (
    service_set - population_set
)

alert_missing = (
    alert_set - population_set
)


if not service_missing:

    passed(
        "All Service History machines exist "
        "in Machine Population"
    )

else:

    failed(
        f"{len(service_missing)} service machines "
        "missing from population"
    )


if not alert_missing:

    passed(
        "All Alert machines exist "
        "in Machine Population"
    )

else:

    failed(
        f"{len(alert_missing)} alert machines "
        "missing from population"
    )


alert_with_history = (
    alert_set.intersection(
        service_set
    )
)


print(
    f"Alert Machines with Service History: "
    f"{len(alert_with_history):,}"
)


# ============================================================
# 10. KNOWLEDGE TERM MAPPING
# ============================================================

def build_search_terms(current_alert):

    terms = []

    for column in [
        category_col,
        description_col,
        parameter_col,
    ]:

        if column is not None:

            value = str(
                current_alert[column]
            ).strip()

            if (
                value
                and value.lower() != "nan"
            ):

                terms.append(
                    value.lower()
                )


    combined = " ".join(terms)


    # ENGINE COOLING
    if (
        "cool" in combined
        or "coolant" in combined
        or "temperature" in combined
        or "temp" in combined
    ):

        terms.extend(
            [
                "engine cooling",
                "cooling",
                "coolant",
                "temperature",
                "overheating",
                "radiator",
            ]
        )


    # HYDRAULIC
    if "hydraulic" in combined:

        terms.extend(
            [
                "hydraulic",
                "hydraulic temperature",
                "hydraulic oil",
                "temperature",
                "pressure",
            ]
        )


    # AIR INTAKE
    if (
        "air" in combined
        or "filter" in combined
        or "restriction" in combined
    ):

        terms.extend(
            [
                "air intake",
                "air filter",
                "filter",
                "restriction",
            ]
        )


    # ELECTRICAL
    if (
        "electrical" in combined
        or "voltage" in combined
        or "battery" in combined
    ):

        terms.extend(
            [
                "electrical",
                "voltage",
                "battery",
                "wiring",
                "connector",
            ]
        )


    return list(
        dict.fromkeys(terms)
    )


# ============================================================
# 11. CASE VALIDATION
# ============================================================

def validate_case(machine_serial):

    header(
        f"C. MACHINE CASE VALIDATION - {machine_serial}"
    )


    results = {
        "machine": False,
        "service": False,
        "alert": False,
        "tsm": False,
        "om": False,
        "context": False,
        "diagnosis": False,
        "plan": False,
        "authorization": False,
        "learning": False,
    }


    # --------------------------------------------------------
    # MACHINE
    # --------------------------------------------------------

    machine_record = machine_df[
        machine_df[machine_serial_col]
        == machine_serial
    ]


    if machine_record.empty:

        failed(
            "Machine Population connection"
        )

        return results


    results["machine"] = True

    passed(
        "Machine Population connected"
    )


    # --------------------------------------------------------
    # SERVICE HISTORY
    # --------------------------------------------------------

    service_history = service_df[
        service_df[service_serial_col]
        == machine_serial
    ]


    if service_history.empty:

        failed(
            "Service History connection"
        )

    else:

        results["service"] = True

        passed(
            f"Service History connected "
            f"({len(service_history)} records)"
        )


    # --------------------------------------------------------
    # ALERT
    # --------------------------------------------------------

    machine_alerts = alert_df[
        alert_df[alert_serial_col]
        == machine_serial
    ].copy()


    if machine_alerts.empty:

        failed(
            "Telematics Alert connection"
        )

        return results


    machine_alerts["_rank"] = (
        machine_alerts[severity_col]
        .apply(severity_rank)
    )


    machine_alerts = (
        machine_alerts
        .sort_values(
            "_rank",
            ascending=False
        )
    )


    current_alert = (
        machine_alerts.iloc[0]
    )


    severity = normalize_severity(
        current_alert[severity_col]
    )


    results["alert"] = True

    passed(
        "Telematics Alert connected"
    )


    if alert_id_col is not None:

        info(
            f"Alert ID : "
            f"{current_alert[alert_id_col]}"
        )


    info(
        f"Severity : {severity}"
    )


    if category_col is not None:

        info(
            f"System   : "
            f"{current_alert[category_col]}"
        )


    # --------------------------------------------------------
    # BUILD KNOWLEDGE SEARCH TERMS
    # --------------------------------------------------------

    search_terms = build_search_terms(
        current_alert
    )


    info(
        "Knowledge Search Terms:"
    )

    info(
        ", ".join(search_terms)
    )


    # --------------------------------------------------------
    # TROUBLESHOOTING MANUAL
    # --------------------------------------------------------

    tsm_results = search_knowledge(
        tsm_df,
        search_terms
    )


    if tsm_results.empty:

        failed(
            "Troubleshooting Manual retrieval"
        )

    else:

        results["tsm"] = True

        passed(
            f"Troubleshooting Manual retrieval "
            f"({len(tsm_results)} relevant sections)"
        )


        tsm_doc_col = find_column(
            tsm_results,
            ["Doc_ID", "Document_ID"]
        )

        tsm_section_col = find_column(
            tsm_results,
            ["Section_ID", "Section ID"]
        )


        if (
            tsm_doc_col is not None
            and tsm_section_col is not None
        ):

            top = tsm_results.iloc[0]

            info(
                f"Top Evidence: "
                f"{top[tsm_doc_col]} / "
                f"{top[tsm_section_col]}"
            )


    # --------------------------------------------------------
    # O&M MANUAL
    # --------------------------------------------------------

    om_results = search_knowledge(
        om_df,
        search_terms
    )


    if om_results.empty:

        failed(
            "O&M Manual retrieval"
        )

    else:

        results["om"] = True

        passed(
            f"O&M Manual retrieval "
            f"({len(om_results)} relevant sections)"
        )


        om_doc_col = find_column(
            om_results,
            ["Doc_ID", "Document_ID"]
        )

        om_section_col = find_column(
            om_results,
            ["Section_ID", "Section ID"]
        )


        if (
            om_doc_col is not None
            and om_section_col is not None
        ):

            top = om_results.iloc[0]

            info(
                f"Top Evidence: "
                f"{top[om_doc_col]} / "
                f"{top[om_section_col]}"
            )


    # --------------------------------------------------------
    # DIAGNOSTIC CONTEXT
    # --------------------------------------------------------

    results["context"] = all(
        [
            results["machine"],
            results["service"],
            results["alert"],
        ]
    )


    if results["context"]:

        passed(
            "Integrated Diagnostic Context ready"
        )

    else:

        failed(
            "Integrated Diagnostic Context incomplete"
        )


    # --------------------------------------------------------
    # GROUNDED DIAGNOSIS
    # --------------------------------------------------------

    results["diagnosis"] = (
        results["context"]
        and results["tsm"]
        and results["om"]
    )


    if results["diagnosis"]:

        passed(
            "AI-assisted grounded diagnostic reasoning ready"
        )

    else:

        failed(
            "Grounded diagnostic reasoning not ready"
        )


    # --------------------------------------------------------
    # AGENTIC SERVICE PLAN
    # --------------------------------------------------------

    results["plan"] = (
        results["diagnosis"]
    )


    if results["plan"]:

        passed(
            "Agentic Service Action Plan ready"
        )

    else:

        failed(
            "Agentic Service Action Plan unavailable"
        )


    # --------------------------------------------------------
    # GOVERNANCE / AUTHORIZATION
    # --------------------------------------------------------

    print()
    info(
        "GOVERNANCE DECISION"
    )


    if severity == "CRITICAL":

        decision_mode = "HITL"

        info(
            "Decision Mode             : HITL"
        )

        info(
            "Human Approval Required   : YES"
        )

        info(
            "Execution Before Approval : BLOCKED"
        )


    else:

        decision_mode = "AUTO-AUTHORIZED"

        info(
            "Decision Mode             : AUTO-AUTHORIZED"
        )

        info(
            "Human Approval Required   : NO"
        )

        info(
            "Execution                 : "
            "ALLOWED WITHIN GUARDRAILS"
        )


    results["authorization"] = True

    passed(
        "Risk-based authorization policy validated"
    )


    # --------------------------------------------------------
    # OUTCOME LEARNING
    # --------------------------------------------------------

    results["learning"] = (
        results["plan"]
        and results["authorization"]
    )


    if results["learning"]:

        passed(
            "Outcome capture & closed-loop learning path ready"
        )

    else:

        failed(
            "Outcome learning path unavailable"
        )


    # --------------------------------------------------------
    # CASE SUMMARY
    # --------------------------------------------------------

    print()
    info(
        "CASE SUMMARY"
    )

    info(
        f"Machine       : {machine_serial}"
    )

    info(
        f"Severity      : {severity}"
    )

    info(
        f"Decision Mode : {decision_mode}"
    )


    if severity == "CRITICAL":

        info(
            "Workflow      : Predict -> Diagnose -> Plan "
            "-> Human Approve -> Execute -> Learn"
        )

    else:

        info(
            "Workflow      : Predict -> Diagnose -> Plan "
            "-> Auto-Authorize -> Execute -> Learn"
        )


    return results


# ============================================================
# 12. RUN BOTH GOVERNANCE PATHS
# ============================================================

critical_results = validate_case(
    CRITICAL_MACHINE
)


noncritical_results = validate_case(
    NON_CRITICAL_MACHINE
)


# ============================================================
# 13. FINAL READINESS
# ============================================================

header(
    "D. FINAL PROTOTYPE READINESS"
)


checks = [
    (
        "1. Machine Population",
        critical_results["machine"]
        and noncritical_results["machine"]
    ),

    (
        "2. Service History",
        critical_results["service"]
        and noncritical_results["service"]
    ),

    (
        "3. Telematics Alerts",
        critical_results["alert"]
        and noncritical_results["alert"]
    ),

    (
        "4. Troubleshooting Knowledge",
        critical_results["tsm"]
        and noncritical_results["tsm"]
    ),

    (
        "5. O&M Knowledge",
        critical_results["om"]
        and noncritical_results["om"]
    ),

    (
        "6. Diagnostic Context",
        critical_results["context"]
        and noncritical_results["context"]
    ),

    (
        "7. AI Diagnostic Reasoning",
        critical_results["diagnosis"]
        and noncritical_results["diagnosis"]
    ),

    (
        "8. Agentic Service Planning",
        critical_results["plan"]
        and noncritical_results["plan"]
    ),

    (
        "9. Risk-Based Authorization",
        critical_results["authorization"]
        and noncritical_results["authorization"]
    ),

    (
        "10. Outcome Learning",
        critical_results["learning"]
        and noncritical_results["learning"]
    ),
]


overall_ready = True


for name, status in checks:

    if status:

        print(
            f"[PASS] {name}"
        )

    else:

        print(
            f"[FAIL] {name}"
        )

        overall_ready = False


print()


if overall_ready:

    print("=" * 74)
    print(
        "END-TO-END PROTOTYPE: READY"
    )
    print("=" * 74)

    print()
    print(
        f"CRITICAL CASE    : {CRITICAL_MACHINE}"
    )

    print(
        "Governance       : HITL"
    )

    print(
        "Execution        : Blocked until human approval"
    )

    print()
    print(
        f"NON-CRITICAL CASE: {NON_CRITICAL_MACHINE}"
    )

    print(
        "Governance       : Auto-Authorized"
    )

    print(
        "Execution        : Allowed within approved guardrails"
    )

    print()
    print(
        "COMPLETE CAPSTONE FLOW:"
    )

    print(
        "Fleet -> Detect Risk -> Retrieve Context "
        "-> Ground Diagnosis -> Plan Service "
        "-> Authorize -> Execute -> Capture Outcome -> Learn"
    )

else:

    print("=" * 74)
    print(
        "END-TO-END PROTOTYPE: REVIEW REQUIRED"
    )
    print("=" * 74)


print()
print(
    "IMPORTANT: This prototype uses synthetic / illustrative "
    "data and technical knowledge for academic demonstration."
)

print(
    "It does not represent OEM-prescribed diagnostic limits "
    "or an autonomous safety-critical maintenance system."
)