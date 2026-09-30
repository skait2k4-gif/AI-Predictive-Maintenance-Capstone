import pandas as pd

# Load the three structured data layers
machines = pd.read_excel(
    "data/01_Machine_Population_3200_XYZ20T.xlsx"
)

service = pd.read_excel(
    "data/02_Machine_Service_History_Integrated.xlsx",
    sheet_name="Machine Service History"
)

alerts = pd.read_excel(
    "data/03_Telematics_Machine_Alarm_Alerts.xlsx"
)

# Convert serial numbers to clean text
machines["Machine_Serial_No"] = machines["Machine_Serial_No"].astype(str).str.strip()
service["Machine_Serial_No"] = service["Machine_Serial_No"].astype(str).str.strip()
alerts["Machine_Serial_No"] = alerts["Machine_Serial_No"].astype(str).str.strip()

# Create unique serial-number sets
machine_serials = set(machines["Machine_Serial_No"])
service_serials = set(service["Machine_Serial_No"])
alert_serials = set(alerts["Machine_Serial_No"])

print("===== CAPSTONE DATA INTEGRITY CHECK =====")

print("\nMachine Population:")
print("Total machines:", len(machine_serials))

print("\nService History:")
print("Unique machines:", len(service_serials))

print("\nTelematics Alerts:")
print("Unique machines:", len(alert_serials))

# Check whether service-history machines exist in population
service_missing = service_serials - machine_serials

print("\nService machines missing from Machine Population:")
print(len(service_missing))

if service_missing:
    print(list(service_missing)[:20])

# Check whether alert machines exist in population
alerts_missing = alert_serials - machine_serials

print("\nAlert machines missing from Machine Population:")
print(len(alerts_missing))

if alerts_missing:
    print(list(alerts_missing)[:20])

# Check alert machines that also have service history
alert_with_history = alert_serials.intersection(service_serials)

print("\nAlert machines having Service History:")
print(len(alert_with_history))

print("\n===== CHECK COMPLETE =====")