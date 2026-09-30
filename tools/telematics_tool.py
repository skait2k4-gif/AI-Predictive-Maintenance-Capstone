import pandas as pd

file_path = "data/03_Telematics_Machine_Alarm_Alerts.xlsx"

alerts = pd.read_excel(file_path)


def get_machine_alerts(machine_serial_no):
    """
    Retrieve telematics alarm alerts
    for a particular machine.
    """

    result = alerts[
        alerts["Machine_Serial_No"]
        .astype(str)
        .str.upper()
        == machine_serial_no.upper()
    ]

    if result.empty:
        return f"No telematics alerts found for {machine_serial_no}"

    # Latest alerts first
    if "Alert_Start_Timestamp" in result.columns:
        result = result.sort_values(
            "Alert_Start_Timestamp",
            ascending=False
        )

    return result.to_dict(orient="records")


# Find a suitable prototype case

critical_cooling = alerts[
    (alerts["Alert_Category"] == "Engine Cooling")
    & (alerts["Severity"] == "Critical")
]

critical_cooling = critical_cooling.sort_values(
    "HMR",
    ascending=False
)

print("\n===== PROTOTYPE SHOWCASE CANDIDATES =====")

print(
    critical_cooling[
        [
            "Machine_Serial_No",
            "Alert_ID",
            "Alert_Start_Timestamp",
            "HMR",
            "Alert_Category",
            "Severity",
            "Parameter_Name",
            "Parameter_Value"
        ]
    ].head(10).to_string(index=False)
)