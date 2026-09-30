# ============================================================
# STEP 20B
# CREATE SYNTHETIC ML-READY PREDICTIVE MAINTENANCE DATASET
#
# Capstone:
# AI-Powered Predictive Maintenance &
# Intelligent Service Management
#
# Primary ML Use Case:
# Predict elevated Engine Cooling / Overheating Risk
# during the NEXT 24 HOURS.
#
# IMPORTANT:
# - Synthetic / illustrative academic data only.
# - Thresholds are NOT OEM-prescribed limits.
# - Machine_Serial_No links this dataset to the existing
#   five-layer Capstone data foundation.
# ============================================================

from pathlib import Path
import numpy as np
import pandas as pd


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

MACHINE_FILE = (
    DATA_DIR / "01_Machine_Population_3200_XYZ20T.xlsx"
)

ALERT_FILE = (
    DATA_DIR / "03_Telematics_Machine_Alarm_Alerts.xlsx"
)

OUTPUT_FILE = (
    DATA_DIR / "06_ML_Ready_Cooling_Risk_Dataset.csv"
)


# ============================================================
# 2. REPRODUCIBILITY
# ============================================================

RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)


# ============================================================
# 3. DATASET DESIGN
# ============================================================

# We deliberately use a subset of the 3,200-machine fleet.
# This keeps the prototype lightweight while preserving
# linkage to the full machine population.

NUMBER_OF_MACHINES = 600

# 60 daily prediction snapshots per machine.
NUMBER_OF_DAYS = 60

START_DATE = pd.Timestamp("2026-06-01")

# Approximate share of machines that will develop a
# synthetic cooling-risk episode during the observation
# period.
RISK_MACHINE_SHARE = 0.25


# ============================================================
# 4. LOAD EXISTING CAPSTONE DATA
# ============================================================

print()
print("=" * 74)
print("STEP 20B - CREATE ML-READY COOLING-RISK DATASET")
print("=" * 74)

print()
print("Loading existing Capstone datasets...")


if not MACHINE_FILE.exists():
    raise FileNotFoundError(
        f"Machine Population file not found:\n{MACHINE_FILE}"
    )


if not ALERT_FILE.exists():
    raise FileNotFoundError(
        f"Telematics Alert file not found:\n{ALERT_FILE}"
    )


machine_df = pd.read_excel(MACHINE_FILE)
alert_df = pd.read_excel(ALERT_FILE)


print(
    f"Machine Population loaded : {len(machine_df):,} rows"
)

print(
    f"Telematics Alerts loaded  : {len(alert_df):,} rows"
)


# ============================================================
# 5. VALIDATE REQUIRED COLUMNS
# ============================================================

required_machine_columns = [
    "Machine_Serial_No",
    "Current_HMR",
]

for column in required_machine_columns:

    if column not in machine_df.columns:
        raise ValueError(
            f"Required Machine Population column missing: {column}"
        )


required_alert_columns = [
    "Machine_Serial_No",
    "Alert_Category",
    "Severity",
]

for column in required_alert_columns:

    if column not in alert_df.columns:
        raise ValueError(
            f"Required Alert column missing: {column}"
        )


machine_df["Machine_Serial_No"] = (
    machine_df["Machine_Serial_No"]
    .astype(str)
    .str.strip()
)

alert_df["Machine_Serial_No"] = (
    alert_df["Machine_Serial_No"]
    .astype(str)
    .str.strip()
)


# ============================================================
# 6. IDENTIFY EXISTING ENGINE-COOLING ALERT MACHINES
# ============================================================

cooling_alert_mask = (
    alert_df["Alert_Category"]
    .astype(str)
    .str.contains(
        "cool",
        case=False,
        na=False
    )
)

cooling_alert_df = alert_df[
    cooling_alert_mask
].copy()


cooling_alert_machines = set(
    cooling_alert_df["Machine_Serial_No"]
    .dropna()
    .astype(str)
)


print()
print(
    f"Existing cooling-alert machines available: "
    f"{len(cooling_alert_machines):,}"
)


# ============================================================
# 7. SELECT 600 MACHINES FROM THE EXISTING FLEET
# ============================================================

population_serials = set(
    machine_df["Machine_Serial_No"]
)


valid_cooling_machines = list(
    cooling_alert_machines.intersection(
        population_serials
    )
)


rng.shuffle(valid_cooling_machines)


number_risk_machines = int(
    NUMBER_OF_MACHINES * RISK_MACHINE_SHARE
)


selected_risk_machines = (
    valid_cooling_machines[
        :number_risk_machines
    ]
)


remaining_machine_df = machine_df[
    ~machine_df["Machine_Serial_No"].isin(
        selected_risk_machines
    )
].copy()


number_control_machines = (
    NUMBER_OF_MACHINES
    - len(selected_risk_machines)
)


control_sample = remaining_machine_df.sample(
    n=number_control_machines,
    random_state=RANDOM_SEED
)


risk_sample = machine_df[
    machine_df["Machine_Serial_No"].isin(
        selected_risk_machines
    )
].copy()


selected_machine_df = pd.concat(
    [
        risk_sample,
        control_sample
    ],
    ignore_index=True
)


selected_machine_df = (
    selected_machine_df
    .drop_duplicates(
        subset=["Machine_Serial_No"]
    )
    .reset_index(drop=True)
)


print()
print(
    f"Selected machines          : "
    f"{len(selected_machine_df):,}"
)

print(
    f"Synthetic risk machines    : "
    f"{len(selected_risk_machines):,}"
)

print(
    f"Control machines           : "
    f"{number_control_machines:,}"
)


# ============================================================
# 8. MACHINE LOOKUP
# ============================================================

machine_lookup = (
    selected_machine_df
    .set_index("Machine_Serial_No")
)


# ============================================================
# 9. GENERATE DAILY TIME-SERIES SNAPSHOTS
# ============================================================

print()
print("Generating daily operating snapshots...")


records = []


for machine_number, machine_serial in enumerate(
    selected_machine_df["Machine_Serial_No"],
    start=1
):

    machine_record = machine_lookup.loc[
        machine_serial
    ]


    current_hmr = pd.to_numeric(
        machine_record.get(
            "Current_HMR",
            3000
        ),
        errors="coerce"
    )


    if pd.isna(current_hmr):
        current_hmr = 3000


    # --------------------------------------------------------
    # MACHINE-SPECIFIC BASELINES
    # --------------------------------------------------------

    baseline_daily_hours = rng.uniform(
        5.0,
        12.0
    )

    baseline_load = rng.uniform(
        45.0,
        75.0
    )

    baseline_coolant = rng.uniform(
        78.0,
        88.0
    )

    baseline_hydraulic_temp = rng.uniform(
        55.0,
        72.0
    )

    baseline_fuel_rate = rng.uniform(
        11.0,
        18.0
    )


    is_risk_machine = (
        machine_serial
        in selected_risk_machines
    )


    # Risk machines receive a synthetic deterioration episode.
    # Event day is intentionally late enough to provide
    # several normal days before deterioration.

    if is_risk_machine:

        event_day = int(
            rng.integers(
                38,
                58
            )
        )

    else:

        event_day = None


    # Estimate HMR at the beginning of our 60-day window.

    estimated_window_hours = (
        baseline_daily_hours
        * NUMBER_OF_DAYS
    )

    start_hmr = max(
        0,
        float(current_hmr)
        - estimated_window_hours
    )


    running_hmr = start_hmr

    daily_coolant_history = []


    for day_index in range(
        NUMBER_OF_DAYS
    ):

        snapshot_date = (
            START_DATE
            + pd.Timedelta(
                days=day_index
            )
        )


        # ----------------------------------------------------
        # ENVIRONMENT & OPERATION
        # ----------------------------------------------------

        ambient_temp = np.clip(
            rng.normal(
                34.0,
                5.0
            ),
            20.0,
            48.0
        )


        daily_hours = np.clip(
            rng.normal(
                baseline_daily_hours,
                1.3
            ),
            2.0,
            16.0
        )


        engine_load = np.clip(
            rng.normal(
                baseline_load,
                8.0
            ),
            25.0,
            98.0
        )


        # ----------------------------------------------------
        # SYNTHETIC DETERIORATION SIGNAL
        # ----------------------------------------------------

        deterioration = 0.0


        if is_risk_machine:

            days_before_event = (
                event_day
                - day_index
            )


            # Gradual abnormal behaviour begins up to
            # 7 days before the synthetic risk event.

            if 0 <= days_before_event <= 7:

                deterioration = (
                    (8 - days_before_event)
                    / 8
                )


            # Event day itself.
            elif days_before_event < 0:

                deterioration = max(
                    0.0,
                    1.0
                    - (
                        abs(days_before_event)
                        / 4
                    )
                )


        # ----------------------------------------------------
        # COOLING BEHAVIOUR
        # ----------------------------------------------------

        coolant_avg = (
            baseline_coolant
            + (engine_load - 60) * 0.08
            + (ambient_temp - 34) * 0.10
            + deterioration * rng.uniform(
                7.0,
                14.0
            )
            + rng.normal(
                0,
                1.2
            )
        )


        coolant_max = (
            coolant_avg
            + rng.uniform(
                3.0,
                7.0
            )
            + deterioration * rng.uniform(
                2.0,
                6.0
            )
        )


        hydraulic_temp = (
            baseline_hydraulic_temp
            + (engine_load - 60) * 0.06
            + (ambient_temp - 34) * 0.08
            + deterioration * rng.uniform(
                1.0,
                4.0
            )
            + rng.normal(
                0,
                1.5
            )
        )


        fuel_rate = (
            baseline_fuel_rate
            + (engine_load - 60) * 0.08
            + deterioration * rng.uniform(
                0.5,
                2.0
            )
            + rng.normal(
                0,
                0.6
            )
        )


        running_hmr += daily_hours


        daily_coolant_history.append(
            coolant_avg
        )


        # ----------------------------------------------------
        # 7-DAY COOLANT TREND
        # ----------------------------------------------------

        if len(
            daily_coolant_history
        ) >= 7:

            recent_values = np.array(
                daily_coolant_history[-7:]
            )

            x = np.arange(
                len(recent_values)
            )

            trend = np.polyfit(
                x,
                recent_values,
                1
            )[0]

        else:

            trend = 0.0


        # ----------------------------------------------------
        # RECENT COOLING ALERT COUNT
        #
        # This is intentionally NOT the future target.
        # It represents known recent history available
        # at prediction time.
        # ----------------------------------------------------

        if (
            is_risk_machine
            and event_day is not None
        ):

            days_before_event = (
                event_day
                - day_index
            )


            if 0 <= days_before_event <= 2:

                recent_cooling_alerts = int(
                    rng.integers(
                        0,
                        2
                    )
                )

            else:

                recent_cooling_alerts = 0

        else:

            recent_cooling_alerts = int(
                rng.random() < 0.01
            )


        # ----------------------------------------------------
        # DAYS SINCE COOLING SERVICE
        # ----------------------------------------------------

        days_since_cooling_service = int(
            np.clip(
                rng.normal(
                    120,
                    70
                )
                + deterioration * 60,
                1,
                450
            )
        )


        # ----------------------------------------------------
        # TARGET:
        # Cooling Risk in NEXT 24 HOURS
        #
        # Positive only on the snapshot immediately before
        # the synthetic event.
        # ----------------------------------------------------

        if (
            is_risk_machine
            and event_day is not None
            and day_index == (
                event_day - 1
            )
        ):

            target_next_24h = 1

        else:

            target_next_24h = 0


        # ----------------------------------------------------
        # CONVENTIONAL ALARM FLAG
        #
        # Simulated conventional alarm occurs at event day,
        # AFTER the predictive target snapshot.
        # This allows the prototype to demonstrate:
        #
        # ML Risk Signal -> BEFORE -> Conventional Alarm
        # ----------------------------------------------------

        conventional_alarm_flag = int(
            is_risk_machine
            and event_day is not None
            and day_index >= event_day
            and day_index <= event_day + 1
        )


        # ----------------------------------------------------
        # DATA QUALITY
        # ----------------------------------------------------

        data_quality_score = np.clip(
            rng.normal(
                0.96,
                0.025
            ),
            0.80,
            1.00
        )


        records.append(
            {
                "Machine_Serial_No":
                    machine_serial,

                "Snapshot_Date":
                    snapshot_date,

                "HMR":
                    round(
                        running_hmr,
                        1
                    ),

                "Daily_Working_Hours":
                    round(
                        daily_hours,
                        2
                    ),

                "Engine_Load_Pct":
                    round(
                        engine_load,
                        2
                    ),

                "Ambient_Temp_C":
                    round(
                        ambient_temp,
                        2
                    ),

                "Coolant_Temp_Avg_C":
                    round(
                        coolant_avg,
                        2
                    ),

                "Coolant_Temp_Max_C":
                    round(
                        coolant_max,
                        2
                    ),

                "Coolant_7Day_Trend_C_Per_Day":
                    round(
                        trend,
                        3
                    ),

                "Hydraulic_Oil_Temp_C":
                    round(
                        hydraulic_temp,
                        2
                    ),

                "Fuel_Rate_LPH":
                    round(
                        fuel_rate,
                        2
                    ),

                "Recent_Cooling_Alerts_7D":
                    recent_cooling_alerts,

                "Days_Since_Cooling_Service":
                    days_since_cooling_service,

                "Data_Quality_Score":
                    round(
                        data_quality_score,
                        3
                    ),

                "Conventional_Alarm_Flag":
                    conventional_alarm_flag,

                "Target_Cooling_Risk_Next_24H":
                    target_next_24h,

                "Synthetic_Risk_Machine":
                    int(
                        is_risk_machine
                    ),

                "Synthetic_Event_Day":
                    (
                        event_day
                        if event_day is not None
                        else ""
                    ),

                "Data_Type":
                    "Synthetic / Illustrative",
            }
        )


# ============================================================
# 10. CREATE DATAFRAME
# ============================================================

ml_df = pd.DataFrame(
    records
)


ml_df["Snapshot_Date"] = pd.to_datetime(
    ml_df["Snapshot_Date"]
)


ml_df = (
    ml_df
    .sort_values(
        [
            "Snapshot_Date",
            "Machine_Serial_No"
        ]
    )
    .reset_index(drop=True)
)


# ============================================================
# 11. BASIC QUALITY CHECKS
# ============================================================

print()
print("=" * 74)
print("DATASET QUALITY CHECK")
print("=" * 74)


total_rows = len(
    ml_df
)

unique_machines = (
    ml_df["Machine_Serial_No"]
    .nunique()
)

positive_targets = int(
    ml_df[
        "Target_Cooling_Risk_Next_24H"
    ].sum()
)

conventional_alarms = int(
    ml_df[
        "Conventional_Alarm_Flag"
    ].sum()
)


print(
    f"Total ML rows                    : "
    f"{total_rows:,}"
)

print(
    f"Unique machines                  : "
    f"{unique_machines:,}"
)

print(
    f"Positive Next-24H risk snapshots : "
    f"{positive_targets:,}"
)

print(
    f"Conventional alarm snapshots     : "
    f"{conventional_alarms:,}"
)


# ============================================================
# 12. REFERENTIAL INTEGRITY
# ============================================================

population_set = set(
    machine_df["Machine_Serial_No"]
)

ml_machine_set = set(
    ml_df["Machine_Serial_No"]
)


missing_machines = (
    ml_machine_set
    - population_set
)


if len(
    missing_machines
) == 0:

    print(
        "[PASS] All ML machines exist "
        "in Machine Population"
    )

else:

    print(
        f"[FAIL] {len(missing_machines)} "
        "ML machines missing from population"
    )


# ============================================================
# 13. LEAKAGE CHECK
# ============================================================

# Target must not itself be used as an input feature later.
# Conventional_Alarm_Flag is retained for demonstration and
# comparison but will be EXCLUDED from the predictive model.

print(
    "[PASS] Target defined as future Next-24H risk"
)

print(
    "[PASS] Conventional alarm retained only for "
    "comparison and will be excluded from ML features"
)


# ============================================================
# 14. SAVE OUTPUT
# ============================================================

ml_df.to_csv(
    OUTPUT_FILE,
    index=False
)


print()
print("=" * 74)
print("STEP 20B COMPLETE")
print("=" * 74)

print()
print(
    f"ML-ready dataset saved to:"
)

print(
    OUTPUT_FILE
)

print()
print(
    "Prediction Question:"
)

print(
    "Based only on information available at the "
    "current snapshot, what is the probability of "
    "elevated Engine Cooling risk during the next 24 hours?"
)

print()
print(
    "IMPORTANT:"
)

print(
    "All values, deterioration patterns and thresholds "
    "are synthetic / illustrative for academic use."
)

print(
    "They are NOT OEM-prescribed operating limits."
)