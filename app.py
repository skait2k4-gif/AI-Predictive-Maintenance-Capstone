# app.py
# ============================================================
# STEP 21A — PROFESSOR DEMO / PRESENTATION-POLISHED VERSION
# AI-Powered Predictive Maintenance & Intelligent Service Management
#
# Replace the existing app.py in AI_Capstone_Agent with this file.
#
# Run:
#   streamlit run app.py
#
# Expected files under ./data/
#   01_Machine_Population_3200_XYZ20T.xlsx
#   02_Machine_Service_History_Integrated.xlsx
#   03_Telematics_Machine_Alarm_Alerts.xlsx
#   04_Synthetic_Troubleshooting_Manual_XYZ20T.xlsx
#   05_Synthetic_Operation_Maintenance_Manual_XYZ20T.xlsx
#   06_ML_Ready_Cooling_Risk_Dataset.csv
#   07_ML_Cooling_Risk_Predictions.csv
#   07_ML_Feature_Importance.csv
#   07_ML_Model_Summary.csv
# ============================================================

from pathlib import Path
from datetime import datetime
import html

import numpy as np
import pandas as pd
import streamlit as st

try:
    import altair as alt
except Exception:
    alt = None


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Predictive Maintenance | Service AI",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PRESENTATION CSS
# ============================================================

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.6rem;
        padding-bottom: 2.2rem;
        max-width: 1500px;
    }

    [data-testid="stSidebar"] {
        min-width: 285px;
        max-width: 285px;
    }

    div[data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,0.28);
        border-radius: 14px;
        padding: 14px 14px 10px 14px;
        min-height: 105px;
    }

    div[data-testid="stMetric"] label {
        font-weight: 650;
    }

    .hero-box {
        border: 1px solid rgba(128,128,128,0.28);
        border-radius: 16px;
        padding: 26px 28px;
        margin: 8px 0 18px 0;
    }

    .hero-title {
        font-size: 1.55rem;
        font-weight: 750;
        line-height: 1.3;
        margin-bottom: 12px;
    }

    .hero-sub {
        font-size: 1.02rem;
        line-height: 1.6;
    }

    .flow-wrap {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 10px;
        margin: 8px 0 22px 0;
    }

    .flow-step {
        border: 1px solid rgba(128,128,128,0.30);
        border-radius: 12px;
        padding: 16px 8px;
        text-align: center;
        font-weight: 700;
    }

    .small-note {
        opacity: 0.76;
        font-size: 0.90rem;
        line-height: 1.5;
    }

    .evidence-card {
        border: 1px solid rgba(128,128,128,0.28);
        border-radius: 14px;
        padding: 18px;
        min-height: 150px;
    }

    .evidence-card h4 {
        margin-top: 0;
        margin-bottom: 10px;
    }

    .governance-box {
        border: 1px solid rgba(128,128,128,0.28);
        border-radius: 14px;
        padding: 18px 20px;
        margin: 12px 0;
    }

    /* Custom text KPI cards: unlike st.metric, these wrap instead of ellipsizing */
    .wrap-kpi {
        border: 1px solid rgba(128,128,128,0.28);
        border-radius: 14px;
        padding: 14px 16px;
        min-height: 112px;
        height: 100%;
        box-sizing: border-box;
        overflow: hidden;
    }
    .wrap-kpi-label {
        font-size: 0.78rem;
        font-weight: 700;
        opacity: 0.86;
        margin-bottom: 9px;
        line-height: 1.15;
    }
    .wrap-kpi-value {
        font-size: 1.20rem;
        font-weight: 600;
        line-height: 1.28;
        white-space: normal !important;
        overflow-wrap: break-word !important;
        word-break: normal !important;
        text-overflow: clip !important;
        overflow: visible !important;
    }
    .machine-kpi-value {
        font-size: 1.08rem;
        font-weight: 650;
        line-height: 1.25;
        white-space: normal !important;
        overflow-wrap: anywhere !important;
    }

    @media (max-width: 1000px) {
        .flow-wrap {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

FILES = {
    "population": DATA_DIR / "01_Machine_Population_3200_XYZ20T.xlsx",
    "service": DATA_DIR / "02_Machine_Service_History_Integrated.xlsx",
    "alerts": DATA_DIR / "03_Telematics_Machine_Alarm_Alerts.xlsx",
    "tsm": DATA_DIR / "04_Synthetic_Troubleshooting_Manual_XYZ20T.xlsx",
    "om": DATA_DIR / "05_Synthetic_Operation_Maintenance_Manual_XYZ20T.xlsx",
    "ml_ready": DATA_DIR / "06_ML_Ready_Cooling_Risk_Dataset.csv",
    "pred": DATA_DIR / "07_ML_Cooling_Risk_Predictions.csv",
    "importance": DATA_DIR / "07_ML_Feature_Importance.csv",
    "summary": DATA_DIR / "07_ML_Model_Summary.csv",
}


# ============================================================
# GENERIC HELPERS
# ============================================================

def first_existing(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None


def safe_text(value, default="-"):
    if value is None:
        return default
    try:
        if pd.isna(value):
            return default
    except Exception:
        pass
    text = str(value).strip()
    return text if text else default


def numeric(series, default=0):
    return pd.to_numeric(series, errors="coerce").fillna(default)


def normalize_severity(value):
    s = safe_text(value, "NO ALERT").upper()
    mapping = {
        "MEDIUM": "MODERATE",
        "MED": "MODERATE",
        "WARNING": "MODERATE",
        "NONE": "NO ALERT",
        "NAN": "NO ALERT",
        "-": "NO ALERT",
    }
    return mapping.get(s, s)


SEVERITY_RANK = {
    "NO ALERT": 0,
    "LOW": 1,
    "MODERATE": 2,
    "HIGH": 3,
    "CRITICAL": 4,
}


def risk_band(prob):
    try:
        p = float(prob)
    except Exception:
        p = 0.0
    if p >= 0.75:
        return "CRITICAL"
    if p >= 0.50:
        return "HIGH"
    if p >= 0.30:
        return "MODERATE"
    return "LOW"


def pct_value(value):
    try:
        x = float(value)
    except Exception:
        return 0.0
    if x <= 1.00001:
        return x * 100
    return x


def dataframe_text(df):
    if df is None or df.empty:
        return pd.Series(dtype=str)
    return (
        df.fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
        .str.lower()
    )


def get_summary_value(summary_df, possible_names, default=np.nan):
    if summary_df is None or summary_df.empty:
        return default

    # Wide one-row format
    for name in possible_names:
        if name in summary_df.columns:
            try:
                return float(summary_df.iloc[0][name])
            except Exception:
                return summary_df.iloc[0][name]

    # Key/value format
    if summary_df.shape[1] >= 2:
        key_col = summary_df.columns[0]
        val_col = summary_df.columns[1]
        keys = summary_df[key_col].astype(str).str.strip().str.lower()

        for name in possible_names:
            mask = keys == str(name).strip().lower()
            if mask.any():
                val = summary_df.loc[mask, val_col].iloc[0]
                try:
                    return float(val)
                except Exception:
                    return val

    return default


def probability_column(df):
    return first_existing(
        df,
        [
            "ML_Risk_Probability",
            "ML_Risk_Prob",
            "Risk_Probability",
            "Predicted_Probability",
            "Probability",
        ],
    )


def ensure_prediction_fields(df):
    out = df.copy()

    serial = first_existing(out, ["Machine_Serial_No", "Machine_Serial", "Serial_No"])
    date_col = first_existing(out, ["Snapshot_Date", "Date", "Prediction_Date"])
    prob_col = probability_column(out)

    if serial and serial != "Machine_Serial_No":
        out = out.rename(columns={serial: "Machine_Serial_No"})

    if date_col:
        out["Snapshot_Date"] = pd.to_datetime(out[date_col], errors="coerce")

    if prob_col:
        out["ML_Risk_Probability"] = pd.to_numeric(out[prob_col], errors="coerce").fillna(0)
        # Protect against files where probability is stored as percentage.
        if out["ML_Risk_Probability"].max() > 1.00001:
            out["ML_Risk_Probability"] = out["ML_Risk_Probability"] / 100.0
    else:
        out["ML_Risk_Probability"] = 0.0

    if "ML_Risk_Pct" not in out.columns:
        out["ML_Risk_Pct"] = (out["ML_Risk_Probability"] * 100).round(1)
    else:
        out["ML_Risk_Pct"] = pd.to_numeric(out["ML_Risk_Pct"], errors="coerce")
        missing = out["ML_Risk_Pct"].isna()
        out.loc[missing, "ML_Risk_Pct"] = (
            out.loc[missing, "ML_Risk_Probability"] * 100
        ).round(1)

    if "ML_Risk_Level" not in out.columns:
        out["ML_Risk_Level"] = out["ML_Risk_Probability"].apply(risk_band)

    if "ML_Predicted_Risk" not in out.columns:
        out["ML_Predicted_Risk"] = (
            out["ML_Risk_Probability"] >= 0.30
        ).astype(int)

    if "Conventional_Alarm_Flag" in out.columns:
        out["Conventional_Alarm_Flag"] = pd.to_numeric(
            out["Conventional_Alarm_Flag"], errors="coerce"
        ).fillna(0).astype(int)

    if "Target_Cooling_Risk_Next_24H" in out.columns:
        out["Target_Cooling_Risk_Next_24H"] = pd.to_numeric(
            out["Target_Cooling_Risk_Next_24H"], errors="coerce"
        ).fillna(0).astype(int)

    return out


def metric_card(label, value, help_text=None):
    st.metric(label, value, help=help_text)


def wrap_kpi(container, label, value, machine=False):
    """Render a text KPI that always wraps and never shows Streamlit ellipsis."""
    value_class = "machine-kpi-value" if machine else "wrap-kpi-value"
    with container:
        st.markdown(
            f'''
            <div class="wrap-kpi">
                <div class="wrap-kpi-label">{html.escape(str(label))}</div>
                <div class="{value_class}">{html.escape(str(value))}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(show_spinner=False)
def load_data():
    missing = [str(p) for p in FILES.values() if not p.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing required data file(s):\n" + "\n".join(missing)
        )

    population = pd.read_excel(FILES["population"], sheet_name=0)

    service_xls = pd.ExcelFile(FILES["service"])
    service_sheet = (
        "Machine Service History"
        if "Machine Service History" in service_xls.sheet_names
        else service_xls.sheet_names[0]
    )
    service = pd.read_excel(FILES["service"], sheet_name=service_sheet)

    alerts = pd.read_excel(FILES["alerts"], sheet_name=0)
    tsm = pd.read_excel(FILES["tsm"], sheet_name=0)
    om = pd.read_excel(FILES["om"], sheet_name=0)

    ml_ready = pd.read_csv(FILES["ml_ready"])
    pred = pd.read_csv(FILES["pred"])
    importance = pd.read_csv(FILES["importance"])
    summary = pd.read_csv(FILES["summary"])

    return population, service, alerts, tsm, om, ml_ready, pred, importance, summary


try:
    (
        population,
        service,
        alerts,
        tsm,
        om,
        ml_ready,
        pred,
        importance,
        summary,
    ) = load_data()
except Exception as exc:
    st.error("The dashboard could not load the required data files.")
    st.code(str(exc))
    st.stop()


# ============================================================
# NORMALIZE CORE DATA
# ============================================================

mserial = first_existing(
    population,
    ["Machine_Serial_No", "Machine_Serial", "Serial_No"],
)
sserial = first_existing(
    service,
    ["Machine_Serial_No", "Machine_Serial", "Serial_No"],
)
aserial = first_existing(
    alerts,
    ["Machine_Serial_No", "Machine_Serial", "Serial_No"],
)

if not mserial or not sserial or not aserial:
    st.error("Machine serial number column could not be identified in one or more source files.")
    st.stop()

population[mserial] = population[mserial].astype(str)
service[sserial] = service[sserial].astype(str)
alerts[aserial] = alerts[aserial].astype(str)

h_m = first_existing(population, ["Current_HMR", "HMR", "Current HMR"])
branchcol = first_existing(population, ["Dealer_Branch", "Branch", "Dealer Branch"])
appcol = first_existing(population, ["Application", "Site_Application"])
customercol = first_existing(population, ["Customer_Name", "Customer"])
sitecol = first_existing(population, ["Site_Name", "Site"])
citycol = first_existing(population, ["City", "Location"])

sevcol = first_existing(alerts, ["Severity", "Alert_Severity", "Risk_Severity"])
aidcol = first_existing(alerts, ["Alert_ID", "Alarm_ID"])
acatcol = first_existing(alerts, ["Alert_Category", "System", "Category"])
adesccol = first_existing(
    alerts,
    ["Alert_Description", "Description", "Symptom_or_Alert"],
)
adatecol = first_existing(
    alerts,
    ["Alert_Start_Timestamp", "Alert_Timestamp", "Timestamp", "Date"],
)

alerts["_sev"] = (
    alerts[sevcol].apply(normalize_severity)
    if sevcol
    else "NO ALERT"
)
alerts["_rank"] = alerts["_sev"].map(SEVERITY_RANK).fillna(0).astype(int)
alerts["_date"] = (
    pd.to_datetime(alerts[adatecol], errors="coerce")
    if adatecol
    else pd.NaT
)

pred = ensure_prediction_fields(pred)
pred["Machine_Serial_No"] = pred["Machine_Serial_No"].astype(str)

ml_ready_serial = first_existing(
    ml_ready,
    ["Machine_Serial_No", "Machine_Serial", "Serial_No"],
)
if ml_ready_serial:
    ml_ready[ml_ready_serial] = ml_ready[ml_ready_serial].astype(str)

if "Snapshot_Date" in ml_ready.columns:
    ml_ready["Snapshot_Date"] = pd.to_datetime(
        ml_ready["Snapshot_Date"], errors="coerce"
    )


# ============================================================
# FLEET SNAPSHOT
# ============================================================

# Current / highest-risk alert representation per machine.
if not alerts.empty:
    current_alerts = (
        alerts.sort_values(
            ["_rank", "_date"],
            ascending=[False, False],
            na_position="last",
        )
        .drop_duplicates(subset=[aserial], keep="first")
        .copy()
    )
else:
    current_alerts = alerts.copy()

fleet = population.copy()

alert_cols = [aserial, "_sev", "_rank"]
for c in [aidcol, acatcol, adesccol, adatecol]:
    if c and c not in alert_cols:
        alert_cols.append(c)

if not current_alerts.empty:
    alert_snapshot = current_alerts[alert_cols].copy()
    if aserial != mserial:
        alert_snapshot = alert_snapshot.rename(columns={aserial: mserial})
    fleet = fleet.merge(alert_snapshot, on=mserial, how="left")

fleet["_sev"] = fleet.get("_sev", pd.Series(index=fleet.index)).fillna("NO ALERT")
fleet["_rank"] = fleet["_sev"].map(SEVERITY_RANK).fillna(0).astype(int)

# Latest ML prediction for each machine.
latest_pred_all = (
    pred.sort_values("Snapshot_Date")
    .drop_duplicates("Machine_Serial_No", keep="last")
    .copy()
)

latest_merge = latest_pred_all[
    [
        c
        for c in [
            "Machine_Serial_No",
            "ML_Risk_Probability",
            "ML_Risk_Pct",
            "ML_Risk_Level",
            "ML_Predicted_Risk",
            "Conventional_Alarm_Flag",
            "Snapshot_Date",
        ]
        if c in latest_pred_all.columns
    ]
].copy()

if mserial != "Machine_Serial_No":
    latest_merge = latest_merge.rename(columns={"Machine_Serial_No": mserial})

fleet = fleet.merge(latest_merge, on=mserial, how="left")

# Peak flagged record per machine.
flagged_pred = pred[pred["ML_Predicted_Risk"].fillna(0).astype(int) == 1].copy()

if not flagged_pred.empty:
    peak_flagged = (
        flagged_pred.sort_values("ML_Risk_Probability", ascending=False)
        .drop_duplicates("Machine_Serial_No", keep="first")
        .copy()
    )
else:
    peak_flagged = flagged_pred.copy()

ml_flagged_machines = set(
    peak_flagged["Machine_Serial_No"].astype(str).unique()
)

# Correct pre-alarm detections.
if {
    "ML_Predicted_Risk",
    "Target_Cooling_Risk_Next_24H",
    "Conventional_Alarm_Flag",
}.issubset(pred.columns):
    prealarm_correct = pred[
        (pred["ML_Predicted_Risk"] == 1)
        & (pred["Target_Cooling_Risk_Next_24H"] == 1)
        & (pred["Conventional_Alarm_Flag"] == 0)
    ].copy()
else:
    prealarm_correct = pd.DataFrame()

prealarm_machines = set(
    prealarm_correct["Machine_Serial_No"].astype(str).unique()
) if not prealarm_correct.empty else set()


# ============================================================
# KPIs / MODEL METRICS
# ============================================================

fleet_population = int(len(population))
machines_with_alerts = int(alerts[aserial].nunique())

severity_machine_counts = (
    current_alerts.groupby("_sev")[aserial].nunique().to_dict()
    if not current_alerts.empty
    else {}
)

critical_count = int(severity_machine_counts.get("CRITICAL", 0))
high_count = int(severity_machine_counts.get("HIGH", 0))
moderate_count = int(severity_machine_counts.get("MODERATE", 0))
low_count = int(severity_machine_counts.get("LOW", 0))

ml_flagged_count = int(len(ml_flagged_machines))
prealarm_machine_count = int(len(prealarm_machines))

ml_cohort_count = (
    int(pred["Machine_Serial_No"].nunique())
    if "Machine_Serial_No" in pred.columns
    else 0
)

precision = get_summary_value(summary, ["Precision", "precision"], 0.217)
recall = get_summary_value(summary, ["Recall", "recall"], 0.811)
f1 = get_summary_value(summary, ["F1", "F1_Score", "f1"], 0.343)
roc_auc = get_summary_value(summary, ["ROC_AUC", "ROC-AUC", "roc_auc"], 0.975)
pr_auc = get_summary_value(summary, ["PR_AUC", "PR-AUC", "pr_auc"], 0.207)
accuracy = get_summary_value(summary, ["Accuracy", "accuracy"], 0.969)
threshold = get_summary_value(
    summary,
    ["Threshold", "Prediction_Threshold", "threshold"],
    0.300,
)

# Confusion matrix / known prototype outputs.
tp = get_summary_value(summary, ["True_Positive", "TP", "True Positive"], np.nan)
tn = get_summary_value(summary, ["True_Negative", "TN", "True Negative"], np.nan)
fp = get_summary_value(summary, ["False_Positive", "FP", "False Positive"], np.nan)
fn = get_summary_value(summary, ["False_Negative", "FN", "False Negative"], np.nan)

# If summary does not contain confusion matrix, calculate from prediction output.
if {
    "ML_Predicted_Risk",
    "Target_Cooling_Risk_Next_24H",
}.issubset(pred.columns):
    yhat = pred["ML_Predicted_Risk"].astype(int)
    y = pred["Target_Cooling_Risk_Next_24H"].astype(int)

    if pd.isna(tp):
        tp = int(((yhat == 1) & (y == 1)).sum())
    if pd.isna(tn):
        tn = int(((yhat == 0) & (y == 0)).sum())
    if pd.isna(fp):
        fp = int(((yhat == 1) & (y == 0)).sum())
    if pd.isna(fn):
        fn = int(((yhat == 0) & (y == 1)).sum())

ml_flagged_snapshots = int((pred["ML_Predicted_Risk"] == 1).sum())

if "Target_Cooling_Risk_Next_24H" in pred.columns:
    correct_risk_detections = int(
        (
            (pred["ML_Predicted_Risk"] == 1)
            & (pred["Target_Cooling_Risk_Next_24H"] == 1)
        ).sum()
    )
else:
    correct_risk_detections = int(tp) if not pd.isna(tp) else 0

prealarm_correct_detections = int(len(prealarm_correct))


# ============================================================
# SESSION STATE
# ============================================================

if "auth" not in st.session_state:
    st.session_state.auth = {}

if "learning" not in st.session_state:
    st.session_state.learning = []


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ Service AI")
st.sidebar.caption("Fleet Service Command Center")

pages = [
    "🏠 Executive Overview",
    "👁 Predictive ML",
    "🚜 Fleet Intelligence",
    "🔎 Machine 360°",
    "📚 AI Diagnosis - RAG",
    "🧠 Agentic Service Plan",
    "🛡️ HITL & Execution",
    "🔄 Outcome & Learning",
    "💰 ROI Simulator",
    "📊 Value & Governance",
]

page = st.sidebar.radio(
    "Navigation",
    pages,
    label_visibility="collapsed",
)

st.sidebar.markdown("---")

all_serials = sorted(population[mserial].dropna().astype(str).unique().tolist())

default_machine = "XYZ20T100388"
default_index = (
    all_serials.index(default_machine)
    if default_machine in all_serials
    else 0
)

# Professor-demo machine selector. This keeps one selected machine as the
# single source of truth, while allowing the presenter to quickly focus on
# Critical/HITL cases without hard-coding individual serial numbers.
critical_serials = sorted(
    current_alerts.loc[current_alerts["_sev"] == "CRITICAL", aserial]
    .dropna().astype(str).unique().tolist()
)

demo_mode = st.sidebar.selectbox(
    "Demo Case Filter",
    ["All Machines", "Critical / HITL Cases"],
    index=0,
    help="Use Critical / HITL Cases during the professor demo to show only machines whose current alert requires human authorization.",
)

selector_serials = critical_serials if demo_mode == "Critical / HITL Cases" else all_serials
if not selector_serials:
    selector_serials = all_serials

preferred_default = default_machine if default_machine in selector_serials else selector_serials[0]
selector_index = selector_serials.index(preferred_default)

selected = st.sidebar.selectbox(
    "Selected Machine",
    selector_serials,
    index=selector_index,
)

if demo_mode == "Critical / HITL Cases":
    st.sidebar.success(f"HITL demo pool: {len(critical_serials)} Critical machines")
    st.sidebar.caption("Critical alert → RAG → Agent plan → Human approval → Simulated execution → Learning")

st.sidebar.markdown("---")
st.sidebar.caption("Synthetic academic prototype")
st.sidebar.caption("ML predicts → RAG grounds → Agent coordinates → Human governs")


# ============================================================
# SELECTED MACHINE CONTEXT
# ============================================================

mrow_df = population[population[mserial].astype(str) == selected]
mrow = mrow_df.iloc[0] if not mrow_df.empty else pd.Series(dtype=object)

msvc = service[service[sserial].astype(str) == selected].copy()
malerts = alerts[alerts[aserial].astype(str) == selected].copy()

if not malerts.empty:
    malerts = malerts.sort_values(
        ["_rank", "_date"],
        ascending=[False, False],
        na_position="last",
    )
    cur_alert = malerts.iloc[0]
    selected_sev = safe_text(cur_alert.get("_sev"), "NO ALERT")
else:
    cur_alert = None
    selected_sev = "NO ALERT"

selected_pred = pred[pred["Machine_Serial_No"].astype(str) == selected].copy()

if not selected_pred.empty:
    selected_pred = selected_pred.sort_values("Snapshot_Date")
    latest_pred = selected_pred.iloc[-1]
    peak_pred = selected_pred.loc[
        selected_pred["ML_Risk_Probability"].idxmax()
    ]
else:
    latest_pred = None
    peak_pred = None

machine_key = selected

# Simplified prototype governance:
# critical current alarm => HITL.
# ML-only elevated risk is treated as a review trigger, not autonomous repair authority.
ml_peak_flag = (
    int(peak_pred.get("ML_Predicted_Risk", 0))
    if peak_pred is not None
    else 0
)

hitl = selected_sev == "CRITICAL"

if machine_key not in st.session_state.auth:
    if hitl:
        st.session_state.auth[machine_key] = {
            "Decision": "PENDING",
            "Work_Order_Status": "NOT RELEASED",
            "Execution_Status": "BLOCKED",
            "Reviewer": "",
            "Remarks": "",
            "Timestamp": "",
        }
    else:
        st.session_state.auth[machine_key] = {
            "Decision": "AUTO_APPROVED",
            "Work_Order_Status": "RELEASED",
            "Execution_Status": "SIMULATED WORK ORDER RELEASED",
            "Reviewer": "AGENT GUARDRAIL POLICY",
            "Remarks": "Routine non-critical action automatically authorized within approved prototype guardrails.",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }


# ============================================================
# RAG HELPERS
# ============================================================

def selected_system():
    if cur_alert is None:
        return ""
    if acatcol:
        return safe_text(cur_alert.get(acatcol), "")
    return ""


def selected_description():
    if cur_alert is None:
        return ""
    if adesccol:
        return safe_text(cur_alert.get(adesccol), "")
    return ""


def rag_terms(system, description):
    text = f"{system} {description}".lower()
    terms = []

    if "hydraulic" in text:
        terms += ["hydraulic", "oil temperature", "hyd"]
    elif "cool" in text or "engine" in text or "overheat" in text:
        terms += ["engine cooling", "coolant", "overheating", "cooling"]
    elif "air" in text or "filter" in text or "restriction" in text:
        terms += ["air intake", "filter", "restriction"]
    elif "electrical" in text or "voltage" in text or "battery" in text:
        terms += ["electrical", "voltage", "battery"]

    # Add useful words from alert text without allowing generic "temperature"
    # to override system relevance.
    for token in text.replace("/", " ").replace("-", " ").split():
        if len(token) >= 5 and token not in {
            "temperature",
            "alert",
            "machine",
            "critical",
            "moderate",
            "warning",
        }:
            terms.append(token)

    return list(dict.fromkeys(terms))


def retrieve_knowledge(df, system, description, top_n=5):
    if df is None or df.empty:
        return pd.DataFrame()

    work = df.copy()

    approval_col = first_existing(
        work,
        ["Approval_Status", "Status", "Approved"],
    )
    if approval_col:
        approved_mask = (
            work[approval_col]
            .fillna("")
            .astype(str)
            .str.upper()
            .str.contains("APPROVED")
        )
        if approved_mask.any():
            work = work[approved_mask].copy()

    if work.empty:
        return work

    terms = rag_terms(system, description)
    row_text = dataframe_text(work)
    score = pd.Series(0.0, index=work.index)

    system_lower = system.lower()

    # Strong system-aware priority.
    if system_lower:
        score += row_text.str.contains(
            system_lower,
            regex=False,
        ).astype(float) * 12

        if "hydraulic" in system_lower:
            score += row_text.str.contains("hydraulic", regex=False).astype(float) * 18
        elif "cool" in system_lower or "engine" in system_lower:
            score += row_text.str.contains("cool", regex=False).astype(float) * 18
        elif "air" in system_lower:
            score += row_text.str.contains("air", regex=False).astype(float) * 18
        elif "electrical" in system_lower:
            score += row_text.str.contains("electrical", regex=False).astype(float) * 18

    for term in terms:
        score += row_text.str.contains(
            str(term).lower(),
            regex=False,
        ).astype(float) * 2

    work["_score"] = score

    relevant = work[work["_score"] > 0].sort_values(
        "_score",
        ascending=False,
    )

    return relevant.head(top_n)


system = selected_system()
description = selected_description()
tsm_res = retrieve_knowledge(tsm, system, description, top_n=5)
om_res = retrieve_knowledge(om, system, description, top_n=5)


def create_service_plan():
    actions = [
        "Review machine condition and validate the risk / alert signal.",
        "Review relevant preventive-maintenance and repair history.",
        "Follow the retrieved troubleshooting inspection sequence before confirming root cause.",
        "Apply the relevant O&M inspection / maintenance guidance.",
    ]

    if selected_sev == "CRITICAL":
        actions.append("Prepare immediate controlled technical intervention plan.")
        actions.append("Block consequential execution until authorized human approval.")
    elif ml_peak_flag == 1 and selected_sev == "NO ALERT":
        actions.append("Schedule a proactive inspection because ML indicates elevated risk before a conventional alarm.")
        actions.append("Do not replace components solely from the ML prediction; validate condition first.")
    else:
        actions.append("Prepare the appropriate routine service / inspection action within approved guardrails.")

    actions.append("Capture technician finding and final outcome for closed-loop learning.")
    return actions


# ============================================================
# COMMON HEADER
# ============================================================

st.title("⚙️ AI-Powered Predictive Maintenance")
st.caption(
    "Heavy Equipment | Classical ML | RAG-Grounded Diagnosis | "
    "Agentic Service Management | Risk-Based HITL"
)

st.info(
    "Academic Capstone prototype using synthetic / illustrative data. "
    "Model metrics and thresholds are not validated OEM performance or OEM-prescribed limits."
)


# ============================================================
# PAGE 1 — EXECUTIVE OVERVIEW
# ============================================================

if page == "🏠 Executive Overview":

    st.header("Executive Service Intelligence")

    st.markdown(
        """
        <div class="hero-box">
            <div class="hero-title">
                From reactive breakdown response to predictive,
                evidence-grounded and intelligently coordinated service
            </div>
            <div class="hero-sub">
                <b>Detect earlier → Diagnose faster → Plan proactively →
                Act intelligently → Learn continuously</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    k = st.columns(6)
    k[0].metric("Fleet Population", f"{fleet_population:,}")
    k[1].metric("Machines with Alerts", f"{machines_with_alerts:,}")
    k[2].metric("Critical", f"{critical_count:,}")
    k[3].metric("High", f"{high_count:,}")
    k[4].metric("ML Flagged", f"{ml_flagged_count:,}")
    k[5].metric("Pre-Alarm Correct Detections", f"{prealarm_correct_detections:,}")

    st.caption(
        f"ML proof-of-concept coverage: {ml_cohort_count:,} machines from the "
        f"{fleet_population:,}-machine synthetic fleet. ML results must not be interpreted "
        "as whole-fleet production performance."
    )

    # Professor demo: surface a small, data-driven shortlist of Critical/HITL cases.
    if critical_serials:
        st.subheader("Professor Demo — Critical Cases Requiring HITL")
        demo_cols = [aserial]
        for c in [acatcol, adesccol, aidcol]:
            if c and c not in demo_cols:
                demo_cols.append(c)
        demo_cases = current_alerts.loc[current_alerts["_sev"] == "CRITICAL", demo_cols].copy().head(5)
        rename_map = {aserial: "Machine"}
        if acatcol: rename_map[acatcol] = "System"
        if adesccol: rename_map[adesccol] = "Alert / Condition"
        if aidcol: rename_map[aidcol] = "Alert ID"
        demo_cases = demo_cases.rename(columns=rename_map)
        demo_cases.insert(1, "Severity", "CRITICAL")
        demo_cases["Governance"] = "HITL REQUIRED"
        st.dataframe(demo_cases, use_container_width=True, hide_index=True)
        st.caption(
            "For the live demo, select ‘Critical / HITL Cases’ in the sidebar, choose any listed machine, "
            "then demonstrate RAG → Agentic Service Plan → HITL & Execution → Outcome & Learning."
        )

    left, right = st.columns([1.15, 1])

    with left:
        st.subheader("Current Fleet Risk")

        risk_df = pd.DataFrame(
            {
                "Risk": ["Critical", "High", "Moderate", "Low"],
                "Machines": [
                    critical_count,
                    high_count,
                    moderate_count,
                    low_count,
                ],
            }
        )

        if alt is not None:
            color_scale = alt.Scale(
                domain=["Critical", "High", "Moderate", "Low"],
                range=["#ef4444", "#f59e0b", "#eab308", "#22c55e"],
            )

            chart = (
                alt.Chart(risk_df)
                .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
                .encode(
                    x=alt.X(
                        "Risk:N",
                        sort=["Critical", "High", "Moderate", "Low"],
                        title=None,
                    ),
                    y=alt.Y("Machines:Q", title="Machines"),
                    color=alt.Color(
                        "Risk:N",
                        scale=color_scale,
                        legend=None,
                    ),
                    tooltip=["Risk:N", "Machines:Q"],
                )
                .properties(height=320)
            )

            st.altair_chart(chart, use_container_width=True)
        else:
            st.bar_chart(risk_df.set_index("Risk"))

    with right:
        st.subheader("Predictive vs Reactive")
        st.markdown(
            f"""
            **Conventional alert:** the condition has already crossed a simulated
            alarm rule.

            **Classical ML:** estimates elevated Engine Cooling risk for the next
            24 hours from operating patterns.

            **Synthetic early-warning demonstration:** **{prealarm_correct_detections}**
            correct ML detections occurred before the simulated conventional alarm
            in the test-period output.

            **Important:** this is a synthetic proof-of-concept result, not a claim
            of real-world OEM predictive performance.
            """
        )

    st.subheader("AI Service Transformation")

    st.markdown(
        """
        <div class="flow-wrap">
            <div class="flow-step">1. Sense</div>
            <div class="flow-step">2. Predict</div>
            <div class="flow-step">3. Diagnose</div>
            <div class="flow-step">4. Plan</div>
            <div class="flow-step">5. Authorize</div>
            <div class="flow-step">6. Execute</div>
            <div class="flow-step">7. Learn</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("What the Prototype Demonstrates")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            """
            <div class="evidence-card">
                <h4>Classical ML</h4>
                Predicts elevated next-24-hour Engine Cooling risk from structured
                operating data.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="evidence-card">
                <h4>RAG</h4>
                Grounds diagnosis and inspection guidance in approved troubleshooting
                and O&M knowledge.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
            <div class="evidence-card">
                <h4>Agentic AI</h4>
                Coordinates context, diagnosis and the next-best service plan rather
                than acting as an uncontrolled autonomous decision-maker.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            """
            <div class="evidence-card">
                <h4>Human Governance</h4>
                Critical / consequential actions are blocked until an authorized
                human decision is recorded.
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# PAGE 2 — PREDICTIVE ML
# ============================================================

elif page == "👁 Predictive ML":

    st.header("Predictive ML — Engine Cooling Risk | Next 24 Hours")

    m = st.columns(3)
    m[0].metric("Precision", f"{float(precision):.3f}")
    m[1].metric("Recall", f"{float(recall):.3f}")
    m[2].metric("Threshold", f"{float(threshold):.3f}")

    st.caption(
        "Precision and Recall show the practical detection trade-off. "
        "The 0.30 threshold is a prototype operating threshold, not an optimized production threshold."
    )

    q = st.columns(4)
    q[0].metric("ML PoC Cohort", f"{ml_cohort_count:,}")
    q[1].metric("ML Flagged Snapshots", f"{ml_flagged_snapshots:,}")
    q[2].metric("Correct Risk Detections", f"{correct_risk_detections:,}")
    q[3].metric("Correct Detections Before Alarm", f"{prealarm_correct_detections:,}")

    st.warning(
        f"Model trade-off: Recall = {float(recall):.1%}, but Precision = "
        f"{float(precision):.1%}. The prototype therefore catches many risk events "
        f"but also generates false-positive inspection workload. Threshold selection "
        "must be validated against business cost, safety and field evidence during pilot."
    )

    left, right = st.columns([1.05, 1])

    with left:
        st.subheader("Top Model Drivers")

        feature_col = first_existing(importance, ["Feature", "feature"])
        imp_pct_col = first_existing(
            importance,
            ["Importance_Pct", "Importance_Percent", "importance_pct"],
        )
        imp_col = first_existing(importance, ["Importance", "importance"])

        if feature_col:
            imp_view = importance.copy()

            if imp_pct_col:
                imp_view["_display_importance"] = pd.to_numeric(
                    imp_view[imp_pct_col], errors="coerce"
                ).fillna(0)
            elif imp_col:
                vals = pd.to_numeric(
                    imp_view[imp_col], errors="coerce"
                ).fillna(0)
                imp_view["_display_importance"] = (
                    vals * 100 if vals.max() <= 1.00001 else vals
                )
            else:
                imp_view["_display_importance"] = 0

            imp_view = imp_view.sort_values(
                "_display_importance",
                ascending=False,
            ).head(12)

            if alt is not None:
                driver_chart = (
                    alt.Chart(imp_view)
                    .mark_bar(cornerRadiusEnd=4)
                    .encode(
                        y=alt.Y(
                            f"{feature_col}:N",
                            sort="-x",
                            title=None,
                        ),
                        x=alt.X(
                            "_display_importance:Q",
                            title="Importance (%)",
                        ),
                        color=alt.Color(
                            f"{feature_col}:N",
                            scale=alt.Scale(scheme="tableau20"),
                            legend=None,
                        ),
                        tooltip=[
                            alt.Tooltip(f"{feature_col}:N", title="Feature"),
                            alt.Tooltip(
                                "_display_importance:Q",
                                title="Importance %",
                                format=".2f",
                            ),
                        ],
                    )
                    .properties(height=390)
                )
                st.altair_chart(driver_chart, use_container_width=True)
            else:
                st.bar_chart(
                    imp_view.set_index(feature_col)[["_display_importance"]]
                )

            display_imp_cols = [
                c for c in [feature_col, imp_col, imp_pct_col] if c
            ]
            st.dataframe(
                imp_view[display_imp_cols],
                use_container_width=True,
                hide_index=True,
                height=300,
            )

    with right:
        st.subheader("Predicted High-Risk Candidates")

        if not peak_flagged.empty:
            high_candidates = peak_flagged.sort_values(
                "ML_Risk_Probability",
                ascending=False,
            ).head(12)

            candidate_cols = [
                c
                for c in [
                    "Machine_Serial_No",
                    "Snapshot_Date",
                    "ML_Risk_Pct",
                    "ML_Risk_Level",
                    "Conventional_Alarm_Flag",
                ]
                if c in high_candidates.columns
            ]

            st.dataframe(
                high_candidates[candidate_cols],
                use_container_width=True,
                hide_index=True,
                height=440,
            )
        else:
            st.info("No ML flagged candidates are available.")

        st.subheader("Validation Trade-Off")

        cm_df = pd.DataFrame(
            {
                "Outcome": [
                    "True Positive",
                    "False Positive",
                    "False Negative",
                    "True Negative",
                ],
                "Count": [
                    int(tp) if not pd.isna(tp) else 0,
                    int(fp) if not pd.isna(fp) else 0,
                    int(fn) if not pd.isna(fn) else 0,
                    int(tn) if not pd.isna(tn) else 0,
                ],
            }
        )

        st.dataframe(
            cm_df,
            use_container_width=True,
            hide_index=True,
        )

    st.subheader(f"Selected Machine ML Trend — {selected}")

    if selected_pred.empty:
        st.info(
            f"{selected} is not part of the {ml_cohort_count:,}-machine ML "
            "demonstration cohort."
        )
    else:
        selected_ml_ready = (
            ml_ready[ml_ready[ml_ready_serial].astype(str) == selected].copy()
            if ml_ready_serial
            else pd.DataFrame()
        )

        trend_cols = [
            c
            for c in [
                "Snapshot_Date",
                "Coolant_Temp_Avg_C",
                "Coolant_Temp_Max_C",
            ]
            if c in selected_ml_ready.columns
        ]

        if len(trend_cols) >= 2:
            trend_data = selected_ml_ready[trend_cols].dropna(
                subset=["Snapshot_Date"]
            )

            if alt is not None:
                melted = trend_data.melt(
                    id_vars=["Snapshot_Date"],
                    var_name="Parameter",
                    value_name="Temperature_C",
                )

                temp_chart = (
                    alt.Chart(melted)
                    .mark_line(point=False)
                    .encode(
                        x=alt.X("Snapshot_Date:T", title="Date"),
                        y=alt.Y("Temperature_C:Q", title="Temperature (°C)"),
                        color=alt.Color(
                            "Parameter:N",
                            scale=alt.Scale(
                                domain=[
                                    "Coolant_Temp_Avg_C",
                                    "Coolant_Temp_Max_C",
                                ],
                                range=[
                                    "#38bdf8",
                                    "#f97316",
                                ],
                            ),
                            title=None,
                        ),
                        tooltip=[
                            "Snapshot_Date:T",
                            "Parameter:N",
                            alt.Tooltip("Temperature_C:Q", format=".1f"),
                        ],
                    )
                    .properties(height=300)
                )

                st.altair_chart(temp_chart, use_container_width=True)
            else:
                st.line_chart(
                    trend_data.set_index("Snapshot_Date")[
                        [c for c in trend_cols if c != "Snapshot_Date"]
                    ]
                )

        if latest_pred is not None and peak_pred is not None:
            a, b, c = st.columns(3)
            a.metric(
                "Latest ML Risk",
                f"{pct_value(latest_pred.get('ML_Risk_Probability', 0)):.1f}%",
            )
            b.metric(
                "Peak Test-Period Risk",
                f"{pct_value(peak_pred.get('ML_Risk_Probability', 0)):.1f}%",
            )
            c.metric(
                "Peak Risk Level",
                safe_text(peak_pred.get("ML_Risk_Level")),
            )

    with st.expander("Professor / Reviewer Notes — ML Limitations"):
        st.write(
            "• Synthetic academic dataset; metrics are illustrative prototype evidence."
        )
        st.write(
            "• Positive risk events are highly imbalanced, so accuracy alone can be misleading."
        )
        st.write(
            "• The fixed 0.30 threshold has not been optimized on a separate business-cost validation process."
        )
        st.write(
            "• Production development should use approved historical data, explicit train/validation/test design, "
            "threshold tuning, calibration, drift monitoring and technical validation."
        )
        st.write(
            "• Recent_Cooling_Alerts_7D is a synthetic feature and should be challenged / revalidated before any production claim."
        )


# ============================================================
# PAGE 3 — FLEET INTELLIGENCE
# ============================================================

elif page == "🚜 Fleet Intelligence":

    st.header("Fleet Risk Intelligence")

    f1, f2, f3 = st.columns(3)

    search_text = f1.text_input(
        "Search machine / customer / site",
        "",
    )

    severity_filter = f2.selectbox(
        "Current Alert Risk",
        [
            "ALL",
            "CRITICAL",
            "HIGH",
            "MODERATE",
            "LOW",
            "NO ALERT",
        ],
    )

    ml_filter = f3.selectbox(
        "ML View",
        [
            "ALL",
            "ML FLAGGED",
            "PRE-ALARM CORRECT DETECTIONS",
            "ML COHORT",
        ],
    )

    view = fleet.copy()

    if severity_filter != "ALL":
        view = view[view["_sev"] == severity_filter].copy()

    if ml_filter == "ML FLAGGED":
        view = view[
            view[mserial].astype(str).isin(ml_flagged_machines)
        ].copy()

        # Replace latest ML display with the machine's peak flagged record.
        peak_display = peak_flagged.copy()
        peak_display["Machine_Serial_No"] = peak_display[
            "Machine_Serial_No"
        ].astype(str)

        merge_cols = [
            c
            for c in [
                "Machine_Serial_No",
                "ML_Risk_Probability",
                "ML_Risk_Pct",
                "ML_Risk_Level",
                "ML_Predicted_Risk",
                "Snapshot_Date",
            ]
            if c in peak_display.columns
        ]

        peak_display = peak_display[merge_cols].drop_duplicates(
            "Machine_Serial_No"
        )

        # Remove existing ML columns before peak merge.
        for c in [
            "ML_Risk_Probability",
            "ML_Risk_Pct",
            "ML_Risk_Level",
            "ML_Predicted_Risk",
            "Snapshot_Date",
        ]:
            if c in view.columns:
                view = view.drop(columns=[c])

        if mserial != "Machine_Serial_No":
            peak_display = peak_display.rename(
                columns={"Machine_Serial_No": mserial}
            )

        view = view.merge(
            peak_display,
            on=mserial,
            how="left",
        )

    elif ml_filter == "PRE-ALARM CORRECT DETECTIONS":
        view = view[
            view[mserial].astype(str).isin(prealarm_machines)
        ].copy()

    elif ml_filter == "ML COHORT":
        cohort = set(pred["Machine_Serial_No"].astype(str).unique())
        view = view[
            view[mserial].astype(str).isin(cohort)
        ].copy()

    if search_text:
        search_columns = [
            c
            for c in [
                mserial,
                customercol,
                sitecol,
                citycol,
                branchcol,
                appcol,
            ]
            if c and c in view.columns
        ]

        mask = (
            view[search_columns]
            .fillna("")
            .astype(str)
            .agg(" ".join, axis=1)
            .str.contains(
                search_text,
                case=False,
                regex=False,
            )
        )
        view = view[mask].copy()

    st.metric("Machines in View", f"{len(view):,}")

    display_columns = [
        c
        for c in [
            mserial,
            h_m,
            branchcol,
            appcol,
            "_sev",
            aidcol,
            acatcol,
            "ML_Risk_Pct",
            "ML_Risk_Level",
            "ML_Predicted_Risk",
        ]
        if c and c in view.columns
    ]

    st.dataframe(
        view.sort_values(
            ["_rank", "ML_Risk_Pct"] if "ML_Risk_Pct" in view.columns else ["_rank"],
            ascending=False,
            na_position="last",
        )[display_columns],
        use_container_width=True,
        hide_index=True,
        height=580,
    )

    st.caption(
        "Use the left-side Selected Machine control to drill into Machine 360°, "
        "RAG Diagnosis, Agentic Service Plan and HITL."
    )


# ============================================================
# PAGE 4 — MACHINE 360
# ============================================================

elif page == "🔎 Machine 360°":

    st.header(f"Machine 360° — {selected}")

    cols = st.columns(5)
    wrap_kpi(cols[0], "Machine", selected, machine=True)
    cols[1].metric(
        "Current HMR",
        safe_text(mrow.get(h_m)) if h_m else "-",
    )
    cols[2].metric("Current Alert Risk", selected_sev)
    cols[3].metric("Service Records", len(msvc))
    cols[4].metric("Alert Records", len(malerts))

    left, right = st.columns(2)

    with left:
        st.subheader("Asset & Operating Context")

        fields = [
            "OEM",
            "Dealer",
            "Dealer_Branch",
            "Model",
            "DOC",
            "Warranty_Status",
            "Telematics_Enabled",
            "Customer_Name",
            "Site_Name",
            "City",
            "Application",
            "Machine_Status",
        ]

        for field in fields:
            if field in mrow.index:
                st.write(
                    f"**{field.replace('_', ' ')}:** "
                    f"{safe_text(mrow[field])}"
                )

    with right:
        st.subheader("Predictive Context")

        if latest_pred is None:
            st.info(
                f"Machine is outside the {ml_cohort_count:,}-machine ML demonstration cohort."
            )
        else:
            st.metric(
                "Latest ML Risk Probability",
                f"{pct_value(latest_pred.get('ML_Risk_Probability', 0)):.1f}%",
            )
            st.write(
                f"**Latest ML Risk Level:** "
                f"{safe_text(latest_pred.get('ML_Risk_Level'))}"
            )
            st.write(
                f"**Predicted Next-24H Risk:** "
                f"{safe_text(latest_pred.get('ML_Predicted_Risk'))}"
            )
            st.write(
                f"**Conventional Alarm Flag:** "
                f"{safe_text(latest_pred.get('Conventional_Alarm_Flag'))}"
            )

            if peak_pred is not None:
                st.write(
                    f"**Peak Test-Period ML Risk:** "
                    f"{pct_value(peak_pred.get('ML_Risk_Probability', 0)):.1f}%"
                )

    st.subheader("Service History")

    if not msvc.empty:
        st.dataframe(
            msvc,
            use_container_width=True,
            hide_index=True,
            height=330,
        )
    else:
        st.info("No service history.")

    st.subheader("Telematics / Alert History")

    if not malerts.empty:
        st.dataframe(
            malerts.drop(
                columns=["_sev", "_rank", "_date"],
                errors="ignore",
            ),
            use_container_width=True,
            hide_index=True,
            height=300,
        )
    else:
        st.info("No alert history.")


# ============================================================
# PAGE 5 — AI DIAGNOSIS / RAG
# ============================================================

elif page == "📚 AI Diagnosis - RAG":

    st.header("AI Diagnostic Assistant — Grounded RAG")

    if cur_alert is None:
        st.info(
            "No conventional alert is available for this selected machine. "
            "If ML has flagged elevated risk, use the prediction as an inspection "
            "trigger rather than inventing a confirmed diagnosis."
        )
    else:
        cols = st.columns(4)
        cols[0].metric("Machine", selected)
        cols[1].metric("System", system or "-")
        cols[2].metric("Severity", selected_sev)
        cols[3].metric(
            "Alert ID",
            safe_text(cur_alert.get(aidcol)) if aidcol else "-",
        )

        st.write(
            f"**Observed condition:** {description or '-'}"
        )

        st.subheader("Troubleshooting Manual Evidence")

        if not tsm_res.empty:
            st.dataframe(
                tsm_res.drop(
                    columns=["_score"],
                    errors="ignore",
                ),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.warning(
                "No sufficiently relevant approved troubleshooting evidence. "
                "Escalate rather than inventing a diagnosis."
            )

        st.subheader("Operation & Maintenance Evidence")

        if not om_res.empty:
            st.dataframe(
                om_res.drop(
                    columns=["_score"],
                    errors="ignore",
                ),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.warning(
                "No sufficiently relevant O&M evidence."
            )

        if not tsm_res.empty or not om_res.empty:
            st.success(
                "Grounded evidence retrieved. Validate the inspection sequence "
                "before confirming root cause or replacing components."
            )

        st.caption(
            "Retrieval is system-aware: Hydraulic alerts are prioritized against "
            "Hydraulic evidence; Engine Cooling alerts against cooling evidence."
        )


# ============================================================
# PAGE 6 — AGENTIC SERVICE PLAN
# ============================================================

elif page == "🧠 Agentic Service Plan":

    st.header("Agentic Service Management")

    cols = st.columns(3)
    cols[0].metric("Current Risk", selected_sev)
    cols[1].metric(
        "Decision Mode",
        "HITL" if hitl else "GUARDRAIL-BASED",
    )
    wrap_kpi(
        cols[2],
        "Agent State",
        "WAITING FOR APPROVAL" if hitl else "READY / AUTO-AUTHORIZED",
    )

    if ml_peak_flag == 1 and selected_sev == "NO ALERT":
        st.info(
            "ML-only early warning: the agent may coordinate a proactive inspection, "
            "but the prediction does not independently prove a fault or authorize "
            "consequential component replacement."
        )

    st.subheader("Proposed Service Plan")

    for index, action in enumerate(
        create_service_plan(),
        start=1,
    ):
        st.write(f"**{index}.** {action}")

    st.subheader("Agent Boundary")

    c1, c2 = st.columns(2)

    with c1:
        st.success(
            "**Agent may:** retrieve context, service history and approved knowledge; "
            "prepare / coordinate a service plan; request approval; execute only "
            "explicitly permitted low-risk workflow steps."
        )

    with c2:
        st.error(
            "**Agent may not:** independently authorize critical / safety / "
            "consequential actions outside the approved authority matrix."
        )

    st.markdown(
        """
        <div class="governance-box">
            <b>Leadership principle:</b> the agent is a controlled orchestrator,
            not an uncontrolled autonomous technical decision-maker.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE 7 — HITL & EXECUTION
# ============================================================

elif page == "🛡️ HITL & Execution":

    st.header("Risk-Based Authorization & Execution")

    if hitl:
        st.error(
            "🔴 HUMAN-IN-THE-LOOP REQUIRED — work order blocked until an authorized decision."
        )

        reviewer = st.text_input(
            "Authorized Reviewer",
            key="reviewer_" + machine_key,
        )

        remarks = st.text_area(
            "Reviewer Remarks / Modification",
            key="remarks_" + machine_key,
        )

        cols = st.columns(4)

        choices = [
            (
                "APPROVE",
                "APPROVED",
                "RELEASED",
                "SIMULATED WORK ORDER RELEASED",
            ),
            (
                "MODIFY",
                "MODIFIED_AND_APPROVED",
                "RELEASED",
                "SIMULATED MODIFIED WORK ORDER RELEASED",
            ),
            (
                "REJECT",
                "REJECTED",
                "NOT RELEASED",
                "BLOCKED",
            ),
            (
                "ESCALATE",
                "ESCALATED",
                "NOT RELEASED",
                "BLOCKED",
            ),
        ]

        for col, (
            label,
            decision,
            work_order,
            execution,
        ) in zip(cols, choices):

            if col.button(
                label,
                use_container_width=True,
            ):
                st.session_state.auth[machine_key] = {
                    "Decision": decision,
                    "Work_Order_Status": work_order,
                    "Execution_Status": execution,
                    "Reviewer": reviewer or "Authorized Reviewer",
                    "Remarks": remarks or label.title(),
                    "Timestamp": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                }
                st.rerun()

    else:
        st.success(
            "🟢 Routine non-critical case — auto-authorized within approved "
            "prototype guardrails."
        )

    auth = st.session_state.auth[machine_key]

    cols = st.columns(3)
    cols[0].metric("Decision", auth["Decision"])
    cols[1].metric("Work Order", auth["Work_Order_Status"])
    cols[2].metric("Execution", auth["Execution_Status"])

    st.write(
        f"**Reviewer / Authority:** {auth.get('Reviewer') or '-'}"
    )
    st.write(
        f"**Remarks:** {auth.get('Remarks') or '-'}"
    )
    st.write(
        f"**Timestamp:** {auth.get('Timestamp') or '-'}"
    )

    st.info(
        "AI: Predict / Retrieve / Diagnose / Recommend / Coordinate\n\n"
        "Human: Approve / Modify / Reject / Escalate consequential actions\n\n"
        "System: Execute only within approved authority and guardrails"
    )


# ============================================================
# PAGE 8 — OUTCOME & LEARNING
# ============================================================

elif page == "🔄 Outcome & Learning":

    st.header("Outcome Capture & Closed-Loop Learning")

    auth = st.session_state.auth[machine_key]
    executable = auth["Work_Order_Status"] == "RELEASED"

    if executable:
        st.success(
            "Work order is executable; outcome can be captured."
        )
    else:
        st.warning(
            "Work order is not released. Outcome capture follows authorization / execution."
        )

    with st.form("learning_" + machine_key):

        finding = st.text_input(
            "Actual Technician Finding"
        )

        root_cause = st.text_input(
            "Confirmed Root Cause"
        )

        repair_action = st.text_input(
            "Repair / Service Action Completed"
        )

        validation = st.selectbox(
            "Post-Service Validation",
            [
                "Not Yet Validated",
                "Condition Restored",
                "Condition Improved",
                "Condition Persists",
                "Escalation Required",
            ],
        )

        useful = st.selectbox(
            "Was AI Recommendation Useful?",
            [
                "Not Assessed",
                "Yes",
                "Partially",
                "No",
            ],
        )

        feedback = st.text_area(
            "Technician Feedback / Learning Note"
        )

        submit = st.form_submit_button(
            "💾 Capture Outcome & Learning"
        )

        if submit:
            if not executable:
                st.warning(
                    "Not saved because the work order is not released."
                )
            else:
                st.session_state.learning.append(
                    {
                        "Timestamp": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "Machine": selected,
                        "Alert_ID": (
                            safe_text(cur_alert.get(aidcol))
                            if cur_alert is not None and aidcol
                            else "-"
                        ),
                        "Severity": selected_sev,
                        "Authorization": auth["Decision"],
                        "Actual_Finding": finding,
                        "Root_Cause": root_cause,
                        "Repair_Action": repair_action,
                        "Validation_Result": validation,
                        "AI_Recommendation_Useful": useful,
                        "Technician_Feedback": feedback,
                    }
                )

                st.success(
                    "Outcome captured in the current prototype session."
                )

    records = [
        record
        for record in st.session_state.learning
        if record["Machine"] == selected
    ]

    if records:
        st.dataframe(
            pd.DataFrame(records),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info(
            "No learning record captured for this machine in the current session."
        )

    st.write(
        "Feedback supports prediction-vs-actual review, false-positive / "
        "false-negative analysis, RAG coverage improvement and service-planning "
        "refinement. It **does not automatically retrain or change the model**."
    )


# ============================================================
# PAGE 9 — ROI SIMULATOR
# ============================================================

elif page == "💰 ROI Simulator":

    st.header("ROI Simulator — Business Value Scenario")
    st.caption(
        "Interactive academic business-case simulator. All assumptions are illustrative "
        "and must be replaced with validated field and finance data before a real investment decision."
    )

    scenario = st.radio(
        "Scenario preset",
        ["Conservative", "Base", "Optimistic"],
        index=1,
        horizontal=True,
        help="Choose a preset, then edit any assumption below to test your own case.",
    )

    presets = {
        "Conservative": {
            "machines": 1000, "breakdowns": 2.0, "downtime_h": 10.0,
            "impact_per_h": 5000, "emergency_premium": 8000,
            "repeat_rate": 20.0, "repeat_cost": 6000,
            "breakdown_reduction": 15.0, "mttr_reduction": 10.0,
            "repeat_reduction": 15.0, "investment_cr": 2.13,
        },
        "Base": {
            "machines": 1000, "breakdowns": 2.0, "downtime_h": 10.0,
            "impact_per_h": 5000, "emergency_premium": 8000,
            "repeat_rate": 20.0, "repeat_cost": 6000,
            "breakdown_reduction": 25.0, "mttr_reduction": 20.0,
            "repeat_reduction": 30.0, "investment_cr": 1.70,
        },
        "Optimistic": {
            "machines": 1000, "breakdowns": 2.0, "downtime_h": 10.0,
            "impact_per_h": 5000, "emergency_premium": 8000,
            "repeat_rate": 20.0, "repeat_cost": 6000,
            "breakdown_reduction": 30.0, "mttr_reduction": 25.0,
            "repeat_reduction": 30.0, "investment_cr": 1.42,
        },
    }
    p = presets[scenario]

    st.subheader("Editable Assumptions")
    a1, a2, a3, a4 = st.columns(4)
    machines = a1.number_input("Fleet size", min_value=1, value=int(p["machines"]), step=100)
    breakdowns = a2.number_input("Breakdowns / machine / year", min_value=0.0, value=float(p["breakdowns"]), step=0.1)
    downtime_h = a3.number_input("Downtime hours / breakdown", min_value=0.0, value=float(p["downtime_h"]), step=1.0)
    impact_per_h = a4.number_input("Economic impact / downtime hour (₹)", min_value=0, value=int(p["impact_per_h"]), step=500)

    b1, b2, b3, b4 = st.columns(4)
    emergency_premium = b1.number_input("Emergency service premium / breakdown (₹)", min_value=0, value=int(p["emergency_premium"]), step=500)
    repeat_rate = b2.number_input("Repeat visit rate (%)", min_value=0.0, max_value=100.0, value=float(p["repeat_rate"]), step=1.0)
    repeat_cost = b3.number_input("Cost / repeat visit (₹)", min_value=0, value=int(p["repeat_cost"]), step=500)
    investment_cr = b4.number_input("Year-1 AI investment (₹ Cr)", min_value=0.01, value=float(p["investment_cr"]), step=0.05, format="%.2f")

    c1, c2, c3 = st.columns(3)
    breakdown_reduction = c1.slider("Breakdown reduction (%)", 0, 60, int(p["breakdown_reduction"]))
    mttr_reduction = c2.slider("MTTR reduction (%)", 0, 60, int(p["mttr_reduction"]))
    repeat_reduction = c3.slider("Repeat-visit reduction (%)", 0, 60, int(p["repeat_reduction"]))

    # Benefit model: avoided breakdown downtime + faster recovery on remaining
    # breakdowns + avoided emergency-service premium + avoided repeat visits.
    annual_breakdowns = machines * breakdowns
    baseline_downtime_cost = annual_breakdowns * downtime_h * impact_per_h
    avoided_breakdown_value = baseline_downtime_cost * breakdown_reduction / 100
    remaining_downtime_cost = baseline_downtime_cost * (1 - breakdown_reduction / 100)
    mttr_value = remaining_downtime_cost * mttr_reduction / 100
    emergency_value = annual_breakdowns * emergency_premium * breakdown_reduction / 100
    repeat_value = annual_breakdowns * (repeat_rate / 100) * repeat_cost * repeat_reduction / 100

    annual_benefit = avoided_breakdown_value + mttr_value + emergency_value + repeat_value
    investment = investment_cr * 10_000_000
    net_benefit = annual_benefit - investment
    roi_pct = (net_benefit / investment * 100) if investment > 0 else 0
    payback_months = (investment / annual_benefit * 12) if annual_benefit > 0 else np.nan
    three_year_benefit = annual_benefit * 3

    st.subheader("Calculated Business Case")
    r = st.columns(5)
    r[0].metric("Year-1 Benefit", f"₹{annual_benefit / 10_000_000:.2f} Cr")
    r[1].metric("Year-1 Investment", f"₹{investment / 10_000_000:.2f} Cr")
    r[2].metric("Net Benefit", f"₹{net_benefit / 10_000_000:.2f} Cr")
    r[3].metric("ROI", f"{roi_pct:.0f}%")
    r[4].metric("Payback", f"{payback_months:.1f} months" if not pd.isna(payback_months) else "-")

    st.info(
        f"Under the **{scenario}** scenario, the simulator estimates approximately "
        f"**₹{annual_benefit / 10_000_000:.2f} Cr** annual benefit against "
        f"**₹{investment / 10_000_000:.2f} Cr** Year-1 investment, producing "
        f"**{roi_pct:.0f}% ROI** with approximately **{payback_months:.1f} months** payback. "
        "This is an illustrative academic scenario, not a financial forecast."
    )

    left, right = st.columns([1.15, 1])
    with left:
        st.subheader("Where the Annual Benefit Comes From")
        benefit_df = pd.DataFrame({
            "Value Driver": [
                "Avoided breakdown downtime",
                "Faster recovery / MTTR",
                "Avoided emergency premium",
                "Reduced repeat visits",
            ],
            "Benefit_Cr": [
                avoided_breakdown_value / 10_000_000,
                mttr_value / 10_000_000,
                emergency_value / 10_000_000,
                repeat_value / 10_000_000,
            ],
        })
        if alt is not None:
            benefit_chart = (
                alt.Chart(benefit_df)
                .mark_bar(cornerRadiusEnd=5)
                .encode(
                    y=alt.Y("Value Driver:N", sort="-x", title=None),
                    x=alt.X("Benefit_Cr:Q", title="Annual benefit (₹ Cr)"),
                    color=alt.Color("Value Driver:N", scale=alt.Scale(scheme="tableau10"), legend=None),
                    tooltip=[
                        alt.Tooltip("Value Driver:N", title="Value driver"),
                        alt.Tooltip("Benefit_Cr:Q", title="₹ Cr", format=".2f"),
                    ],
                )
                .properties(height=320)
            )
            st.altair_chart(benefit_chart, use_container_width=True)
        else:
            st.bar_chart(benefit_df.set_index("Value Driver"))

    with right:
        st.subheader("Executive Economics")
        economics = pd.DataFrame({
            "Measure": ["Annual benefit", "Year-1 investment", "Net Year-1 benefit", "3-year gross benefit"],
            "₹ Cr": [
                annual_benefit / 10_000_000,
                investment / 10_000_000,
                net_benefit / 10_000_000,
                three_year_benefit / 10_000_000,
            ],
        })
        st.dataframe(economics.round(2), use_container_width=True, hide_index=True)
        st.markdown(
            "**Management interpretation**  "
            "\n\nValue is created through fewer breakdowns, shorter recovery time, "
            "lower emergency-service effort and fewer repeat visits. The pilot should "
            "validate each driver separately before the business case is approved."
        )

    st.subheader("Scenario Comparison")
    comparison_rows = []
    for name, sp in presets.items():
        ab = sp["machines"] * sp["breakdowns"]
        base_dt = ab * sp["downtime_h"] * sp["impact_per_h"]
        b1v = base_dt * sp["breakdown_reduction"] / 100
        b2v = base_dt * (1 - sp["breakdown_reduction"] / 100) * sp["mttr_reduction"] / 100
        b3v = ab * sp["emergency_premium"] * sp["breakdown_reduction"] / 100
        b4v = ab * (sp["repeat_rate"] / 100) * sp["repeat_cost"] * sp["repeat_reduction"] / 100
        benefit = b1v + b2v + b3v + b4v
        inv = sp["investment_cr"] * 10_000_000
        comparison_rows.append({
            "Scenario": name,
            "Annual Benefit (₹ Cr)": round(benefit / 10_000_000, 2),
            "Investment (₹ Cr)": round(inv / 10_000_000, 2),
            "Net Benefit (₹ Cr)": round((benefit - inv) / 10_000_000, 2),
            "ROI": f"{((benefit - inv) / inv * 100):.0f}%",
            "Payback": f"{(inv / benefit * 12):.1f} months",
        })
    st.dataframe(pd.DataFrame(comparison_rows), use_container_width=True, hide_index=True)

    st.warning(
        "Keep customer economic value separate from OEM / service-provider cash ROI. "
        "For a real pilot, replace every assumption with approved downtime, failure, "
        "labour, parts, integration, review-workload and adoption data."
    )


# ============================================================
# PAGE 10 — VALUE & GOVERNANCE
# ============================================================

elif page == "📊 Value & Governance":

    st.header("Value, Governance & Pilot Readiness")

    st.subheader("Leadership Dashboard")

    cols = st.columns(5)

    leadership = [
        ("VALUE", "Downtime / MTTR / FTF"),
        ("QUALITY", "Precision / Recall / usefulness"),
        ("COST", "AI + integration + review"),
        ("RISK", "Safety / false negatives / authority"),
        ("ADOPTION", "Engineer usage / overrides"),
    ]

    for col, (heading, description) in zip(cols, leadership):
        wrap_kpi(col, heading, description)

    st.subheader("Current Prototype Evidence")

    evidence_left, evidence_right = st.columns(2)

    with evidence_left:
        st.write(
            "• **Five-layer data foundation:** Machine Population, Service History, "
            "Telematics Alerts, Troubleshooting Manual and O&M Manual."
        )
        st.write(
            "• **Classical ML:** next-24-hour Engine Cooling risk demonstration."
        )
        st.write(
            "• **RAG:** approved synthetic troubleshooting / O&M evidence retrieval."
        )

    with evidence_right:
        st.write(
            "• **Agentic workflow:** prepares and coordinates next-best service action."
        )
        st.write(
            "• **Risk-based governance:** critical / consequential → HITL; "
            "routine non-critical → guardrail-based authorization."
        )
        st.write(
            "• **Closed-loop learning:** outcome capture for later evaluation "
            "and controlled improvement."
        )

    st.subheader("Pilot Decision Framework")

    p = st.columns(5)
    wrap_kpi(p[0], "VALUE", "Business benefit")
    wrap_kpi(p[1], "QUALITY", "Model + RAG")
    wrap_kpi(p[2], "COST", "Full economics")
    wrap_kpi(p[3], "RISK", "Governed")
    wrap_kpi(p[4], "ADOPTION", "Field use")

    st.write(
        "**Pilot decision:** Proceed / Modify / Extend / Defer / Stop — based on "
        "measured evidence rather than technology capability alone."
    )

    st.subheader("Recommended Deployment Path")

    st.markdown(
        """
        <div class="flow-wrap" style="grid-template-columns: repeat(5, 1fr);">
            <div class="flow-step">PoC</div>
            <div class="flow-step">Shadow Validation</div>
            <div class="flow-step">Controlled Live Pilot</div>
            <div class="flow-step">Production</div>
            <div class="flow-step">Scale & Optimize</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.warning(
        "Prototype completion does not equal production readiness. Real deployment "
        "requires approved real data, security / API integration, technical validation, "
        "operating thresholds, model monitoring, governance and pilot evidence."
    )

    with st.expander("Five-Layer Data Foundation"):
        st.write(
            "**1 Machine Population** — asset / customer / site / application context"
        )
        st.write(
            "**2 Service History** — PM, complaints, repairs and prior actions"
        )
        st.write(
            "**3 Telematics / Alerts** — operating condition and alarm signals"
        )
        st.write(
            "**4 Troubleshooting Manual** — grounded diagnostic knowledge"
        )
        st.write(
            "**5 Operation & Maintenance Manual** — grounded maintenance / operating guidance"
        )

    with st.expander("Governance & Accountability"):
        st.write(
            "**AI may:** predict, retrieve, summarize, recommend and coordinate."
        )
        st.write(
            "**Human authority:** approves / modifies / rejects / escalates "
            "critical and consequential actions."
        )
        st.write(
            "**System execution:** limited to approved permissions, authority matrix "
            "and guardrails."
        )
        st.write(
            "**Auditability:** retain prediction, evidence, recommendation, human "
            "decision, execution and outcome."
        )

    with st.expander("ML Performance — Synthetic PoC"):
        perf = pd.DataFrame(
            {
                "Metric": [
                    "Accuracy",
                    "Precision",
                    "Recall",
                    "F1",
                    "ROC-AUC",
                    "PR-AUC",
                    "False Positives",
                    "False Negatives",
                ],
                "Value": [
                    f"{float(accuracy):.3f}",
                    f"{float(precision):.3f}",
                    f"{float(recall):.3f}",
                    f"{float(f1):.3f}",
                    f"{float(roc_auc):.3f}",
                    f"{float(pr_auc):.3f}",
                    str(int(fp) if not pd.isna(fp) else "-"),
                    str(int(fn) if not pd.isna(fn) else "-"),
                ],
            }
        )
        st.dataframe(
            perf,
            use_container_width=True,
            hide_index=True,
        )
        st.caption(
            "Do not present accuracy alone. For this imbalanced predictive-maintenance "
            "prototype, Recall, Precision, PR-AUC, false positives and false negatives "
            "are more decision-relevant."
        )


# ============================================================
# FINAL FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "FINAL | Professor Demo + ROI Simulator | Fleet Service Command Center | "
    "Synthetic academic prototype — not an OEM diagnostic or safety system."
)
