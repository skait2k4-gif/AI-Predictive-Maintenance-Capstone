# ============================================================
# STEP 20C
# CLASSICAL ML - ENGINE COOLING RISK PREDICTION
#
# Capstone:
# AI-Powered Predictive Maintenance &
# Intelligent Service Management
#
# Objective:
# Predict elevated Engine Cooling / Overheating Risk
# during the NEXT 24 HOURS.
#
# IMPORTANT:
# - Synthetic / illustrative academic prototype.
# - NOT an OEM diagnostic model.
# - NOT an OEM-prescribed operating threshold.
# ============================================================

from pathlib import Path
import warnings

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report,
)

warnings.filterwarnings("ignore")


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

INPUT_FILE = (
    DATA_DIR / "06_ML_Ready_Cooling_Risk_Dataset.csv"
)

PREDICTION_OUTPUT_FILE = (
    DATA_DIR / "07_ML_Cooling_Risk_Predictions.csv"
)

FEATURE_IMPORTANCE_FILE = (
    DATA_DIR / "07_ML_Feature_Importance.csv"
)

MODEL_SUMMARY_FILE = (
    DATA_DIR / "07_ML_Model_Summary.csv"
)


# ============================================================
# 2. MODEL SETTINGS
# ============================================================

RANDOM_SEED = 42

# Risk probability threshold used to convert probability
# into a Yes / No prediction.
PREDICTION_THRESHOLD = 0.30


# ============================================================
# 3. FEATURE DEFINITION
# ============================================================

FEATURES = [
    "HMR",
    "Daily_Working_Hours",
    "Engine_Load_Pct",
    "Ambient_Temp_C",
    "Coolant_Temp_Avg_C",
    "Coolant_Temp_Max_C",
    "Coolant_7Day_Trend_C_Per_Day",
    "Hydraulic_Oil_Temp_C",
    "Fuel_Rate_LPH",
    "Recent_Cooling_Alerts_7D",
    "Days_Since_Cooling_Service",
    "Data_Quality_Score",
]

TARGET = "Target_Cooling_Risk_Next_24H"


# ============================================================
# 4. HELPER FUNCTION - RISK LEVEL
# ============================================================

def probability_to_risk_level(probability):

    if probability >= 0.75:
        return "CRITICAL"

    elif probability >= 0.50:
        return "HIGH"

    elif probability >= 0.30:
        return "MODERATE"

    else:
        return "LOW"


# ============================================================
# 5. LOAD DATA
# ============================================================

print()
print("=" * 78)
print("STEP 20C - CLASSICAL ML PREDICTIVE MAINTENANCE")
print("=" * 78)

print()
print("Use Case:")
print(
    "Predict elevated Engine Cooling risk during "
    "the NEXT 24 HOURS."
)

print()
print(
    "NOTE: Synthetic / illustrative academic data only."
)

print(
    "This is not an OEM diagnostic model or "
    "OEM-prescribed operating limit."
)


if not INPUT_FILE.exists():

    raise FileNotFoundError(
        f"\nML-ready dataset not found:\n{INPUT_FILE}\n"
        "Run Step 20B first."
    )


df = pd.read_csv(
    INPUT_FILE
)


print()
print("-" * 78)
print("A. DATASET LOADED")
print("-" * 78)

print(
    f"Total prediction snapshots : {len(df):,}"
)

print(
    f"Unique machines            : "
    f"{df['Machine_Serial_No'].nunique():,}"
)

print(
    f"Positive Next-24H targets  : "
    f"{int(df[TARGET].sum()):,}"
)


# ============================================================
# 6. DATA VALIDATION
# ============================================================

required_columns = (
    ["Machine_Serial_No", "Snapshot_Date"]
    + FEATURES
    + [
        TARGET,
        "Conventional_Alarm_Flag",
    ]
)


missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]


if missing_columns:

    raise ValueError(
        "\nRequired columns are missing:\n"
        + "\n".join(missing_columns)
    )


df["Snapshot_Date"] = pd.to_datetime(
    df["Snapshot_Date"]
)


for column in FEATURES + [TARGET]:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# Replace missing feature values with median values.

for column in FEATURES:

    median_value = df[column].median()

    df[column] = df[column].fillna(
        median_value
    )


df[TARGET] = (
    df[TARGET]
    .fillna(0)
    .astype(int)
)


df = (
    df
    .sort_values(
        [
            "Snapshot_Date",
            "Machine_Serial_No",
        ]
    )
    .reset_index(drop=True)
)


print()
print("[PASS] Required ML columns available")
print("[PASS] Snapshot dates converted")
print("[PASS] Missing feature values handled")


# ============================================================
# 7. LEAKAGE CONTROL
# ============================================================

print()
print("-" * 78)
print("B. LEAKAGE CONTROL")
print("-" * 78)

print(
    "[PASS] Future target is NOT included "
    "in predictor features"
)

print(
    "[PASS] Conventional_Alarm_Flag is NOT included "
    "in predictor features"
)

print(
    "[PASS] Synthetic_Risk_Machine is NOT included "
    "in predictor features"
)

print(
    "[PASS] Synthetic_Event_Day is NOT included "
    "in predictor features"
)


# ============================================================
# 8. TIME-BASED TRAIN / TEST SPLIT
# ============================================================

unique_dates = np.array(
    sorted(
        df["Snapshot_Date"]
        .dropna()
        .unique()
    )
)


if len(unique_dates) < 10:

    raise ValueError(
        "Not enough dates for time-based validation."
    )


# First 75% of dates = training
# Last 25% of dates = future test period.

split_index = int(
    len(unique_dates) * 0.75
)


train_dates = unique_dates[
    :split_index
]

test_dates = unique_dates[
    split_index:
]


train_end_date = pd.Timestamp(
    train_dates[-1]
)

test_start_date = pd.Timestamp(
    test_dates[0]
)


train_df = df[
    df["Snapshot_Date"]
    <= train_end_date
].copy()


test_df = df[
    df["Snapshot_Date"]
    >= test_start_date
].copy()


print()
print("-" * 78)
print("C. TIME-BASED VALIDATION")
print("-" * 78)

print(
    f"Training period : "
    f"{train_df['Snapshot_Date'].min().date()} "
    f"to "
    f"{train_df['Snapshot_Date'].max().date()}"
)

print(
    f"Testing period  : "
    f"{test_df['Snapshot_Date'].min().date()} "
    f"to "
    f"{test_df['Snapshot_Date'].max().date()}"
)

print(
    f"Training rows   : {len(train_df):,}"
)

print(
    f"Testing rows    : {len(test_df):,}"
)

print(
    f"Training positive cases : "
    f"{int(train_df[TARGET].sum()):,}"
)

print(
    f"Testing positive cases  : "
    f"{int(test_df[TARGET].sum()):,}"
)


# ============================================================
# 9. SAFETY CHECK - TARGET EXISTS IN BOTH PERIODS
# ============================================================

if train_df[TARGET].nunique() < 2:

    raise ValueError(
        "\nTraining period contains only one target class.\n"
        "The synthetic event timing must be adjusted "
        "before training."
    )


if test_df[TARGET].nunique() < 2:

    raise ValueError(
        "\nTesting period contains only one target class.\n"
        "The synthetic event timing must be adjusted "
        "before validation."
    )


# ============================================================
# 10. PREPARE TRAINING DATA
# ============================================================

X_train = train_df[
    FEATURES
].copy()

y_train = train_df[
    TARGET
].copy()


X_test = test_df[
    FEATURES
].copy()

y_test = test_df[
    TARGET
].copy()


# ============================================================
# 11. TRAIN RANDOM FOREST MODEL
# ============================================================

print()
print("-" * 78)
print("D. MODEL TRAINING")
print("-" * 78)

print(
    "Training Random Forest classifier..."
)


model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=RANDOM_SEED,
    n_jobs=-1,
)


model.fit(
    X_train,
    y_train
)


print(
    "[PASS] Random Forest model trained"
)


# ============================================================
# 12. PREDICT FUTURE TEST PERIOD
# ============================================================

test_probability = (
    model.predict_proba(
        X_test
    )[:, 1]
)


test_prediction = (
    test_probability
    >= PREDICTION_THRESHOLD
).astype(int)


# ============================================================
# 13. PERFORMANCE METRICS
# ============================================================

accuracy = accuracy_score(
    y_test,
    test_prediction
)

precision = precision_score(
    y_test,
    test_prediction,
    zero_division=0,
)

recall = recall_score(
    y_test,
    test_prediction,
    zero_division=0,
)

f1 = f1_score(
    y_test,
    test_prediction,
    zero_division=0,
)

roc_auc = roc_auc_score(
    y_test,
    test_probability
)

pr_auc = average_precision_score(
    y_test,
    test_probability
)


cm = confusion_matrix(
    y_test,
    test_prediction
)


tn, fp, fn, tp = cm.ravel()


print()
print("-" * 78)
print("E. FUTURE-PERIOD MODEL PERFORMANCE")
print("-" * 78)

print(
    f"Decision Threshold : "
    f"{PREDICTION_THRESHOLD:.2f}"
)

print()
print(
    f"Accuracy   : {accuracy:.3f}"
)

print(
    f"Precision  : {precision:.3f}"
)

print(
    f"Recall     : {recall:.3f}"
)

print(
    f"F1 Score   : {f1:.3f}"
)

print(
    f"ROC-AUC    : {roc_auc:.3f}"
)

print(
    f"PR-AUC     : {pr_auc:.3f}"
)


# ============================================================
# 14. CONFUSION MATRIX
# ============================================================

print()
print("Confusion Matrix")
print("-" * 40)

print(
    f"True Negative  : {tn:,}"
)

print(
    f"False Positive : {fp:,}"
)

print(
    f"False Negative : {fn:,}"
)

print(
    f"True Positive  : {tp:,}"
)


print()
print("Classification Report")
print("-" * 40)

print(
    classification_report(
        y_test,
        test_prediction,
        digits=3,
        zero_division=0,
    )
)


# ============================================================
# 15. FEATURE IMPORTANCE
# ============================================================

feature_importance_df = pd.DataFrame(
    {
        "Feature": FEATURES,
        "Importance":
            model.feature_importances_,
    }
)


feature_importance_df = (
    feature_importance_df
    .sort_values(
        "Importance",
        ascending=False,
    )
    .reset_index(drop=True)
)


feature_importance_df[
    "Importance_Pct"
] = (
    feature_importance_df[
        "Importance"
    ]
    * 100
).round(2)


print()
print("-" * 78)
print("F. TOP MODEL DRIVERS")
print("-" * 78)


for _, row in feature_importance_df.head(
    10
).iterrows():

    print(
        f"{row['Feature']:<35}"
        f"{row['Importance_Pct']:>8.2f}%"
    )


# ============================================================
# 16. CREATE TEST-PERIOD PREDICTION OUTPUT
# ============================================================

prediction_df = test_df[
    [
        "Machine_Serial_No",
        "Snapshot_Date",
        "HMR",
        "Coolant_Temp_Avg_C",
        "Coolant_Temp_Max_C",
        "Coolant_7Day_Trend_C_Per_Day",
        "Engine_Load_Pct",
        "Ambient_Temp_C",
        "Recent_Cooling_Alerts_7D",
        "Conventional_Alarm_Flag",
        TARGET,
    ]
].copy()


prediction_df[
    "ML_Risk_Probability"
] = np.round(
    test_probability,
    4
)


prediction_df[
    "ML_Risk_Pct"
] = np.round(
    test_probability * 100,
    1
)


prediction_df[
    "ML_Predicted_Risk"
] = test_prediction


prediction_df[
    "ML_Risk_Level"
] = [
    probability_to_risk_level(
        probability
    )
    for probability in test_probability
]


# ============================================================
# 17. IDENTIFY HIGH-RISK MACHINE SNAPSHOTS
# ============================================================

high_risk_df = prediction_df[
    prediction_df[
        "ML_Risk_Probability"
    ]
    >= PREDICTION_THRESHOLD
].copy()


high_risk_df = (
    high_risk_df
    .sort_values(
        [
            "ML_Risk_Probability",
            "Snapshot_Date",
        ],
        ascending=[
            False,
            True,
        ],
    )
)


print()
print("-" * 78)
print("G. PREDICTED HIGH-RISK SNAPSHOTS")
print("-" * 78)

print(
    f"High-risk predictions : "
    f"{len(high_risk_df):,}"
)

print(
    f"Machines flagged      : "
    f"{high_risk_df['Machine_Serial_No'].nunique():,}"
)


if len(high_risk_df) > 0:

    display_columns = [
        "Machine_Serial_No",
        "Snapshot_Date",
        "ML_Risk_Pct",
        "ML_Risk_Level",
        TARGET,
        "Conventional_Alarm_Flag",
    ]

    print()
    print(
        high_risk_df[
            display_columns
        ]
        .head(15)
        .to_string(
            index=False
        )
    )


# ============================================================
# 18. PREDICTION VS CONVENTIONAL ALARM DEMONSTRATION
# ============================================================

print()
print("-" * 78)
print("H. PREDICTIVE VS REACTIVE DEMONSTRATION")
print("-" * 78)


true_positive_df = prediction_df[
    (
        prediction_df[
            "ML_Predicted_Risk"
        ] == 1
    )
    &
    (
        prediction_df[
            TARGET
        ] == 1
    )
].copy()


before_alarm_count = int(
    (
        true_positive_df[
            "Conventional_Alarm_Flag"
        ] == 0
    ).sum()
)


print(
    f"Correct ML risk detections       : "
    f"{len(true_positive_df):,}"
)

print(
    f"Detected before conventional alarm: "
    f"{before_alarm_count:,}"
)


if before_alarm_count > 0:

    print()
    print(
        "[PASS] Prototype demonstrates "
        "predictive early-warning behaviour."
    )

    print(
        "       ML identifies elevated risk "
        "before the simulated conventional alarm."
    )

else:

    print()
    print(
        "[REVIEW] No pre-alarm true-positive "
        "examples found in the future test period."
    )


# ============================================================
# 19. SAVE OUTPUT FILES
# ============================================================

prediction_df.to_csv(
    PREDICTION_OUTPUT_FILE,
    index=False,
)


feature_importance_df.to_csv(
    FEATURE_IMPORTANCE_FILE,
    index=False,
)


summary_df = pd.DataFrame(
    [
        {
            "Model":
                "Random Forest",

            "Use_Case":
                "Engine Cooling Risk - Next 24H",

            "Training_Start":
                train_df[
                    "Snapshot_Date"
                ].min(),

            "Training_End":
                train_df[
                    "Snapshot_Date"
                ].max(),

            "Test_Start":
                test_df[
                    "Snapshot_Date"
                ].min(),

            "Test_End":
                test_df[
                    "Snapshot_Date"
                ].max(),

            "Training_Rows":
                len(train_df),

            "Testing_Rows":
                len(test_df),

            "Decision_Threshold":
                PREDICTION_THRESHOLD,

            "Accuracy":
                round(
                    accuracy,
                    4
                ),

            "Precision":
                round(
                    precision,
                    4
                ),

            "Recall":
                round(
                    recall,
                    4
                ),

            "F1":
                round(
                    f1,
                    4
                ),

            "ROC_AUC":
                round(
                    roc_auc,
                    4
                ),

            "PR_AUC":
                round(
                    pr_auc,
                    4
                ),

            "True_Negative":
                int(tn),

            "False_Positive":
                int(fp),

            "False_Negative":
                int(fn),

            "True_Positive":
                int(tp),

            "Pre_Alarm_Correct_Detections":
                before_alarm_count,

            "Data_Type":
                "Synthetic / Illustrative",
        }
    ]
)


summary_df.to_csv(
    MODEL_SUMMARY_FILE,
    index=False,
)


print()
print("-" * 78)
print("I. OUTPUT FILES CREATED")
print("-" * 78)

print(
    f"1. Predictions:\n"
    f"   {PREDICTION_OUTPUT_FILE}"
)

print()
print(
    f"2. Feature Importance:\n"
    f"   {FEATURE_IMPORTANCE_FILE}"
)

print()
print(
    f"3. Model Summary:\n"
    f"   {MODEL_SUMMARY_FILE}"
)


# ============================================================
# 20. FINAL STATUS
# ============================================================

print()
print("=" * 78)
print("STEP 20C COMPLETE")
print("=" * 78)

print()
print(
    "CLASSICAL ML PREDICTIVE LAYER: READY"
)

print()
print(
    "CAPSTONE AI FLOW:"
)

print(
    "Operating Data"
    " -> ML Predicts Risk"
    " -> RAG Grounds Diagnosis"
    " -> Agent Plans Service"
    " -> HITL / Guardrails"
    " -> Execute"
    " -> Learn"
)

print()
print(
    "IMPORTANT:"
)

print(
    "Model performance is based on synthetic / "
    "illustrative academic data."
)

print(
    "Metrics must NOT be presented as validated "
    "real-world OEM performance."
)