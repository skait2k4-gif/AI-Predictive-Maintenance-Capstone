from machine_tool import get_machine_details
from service_history_tool import get_service_history
from telematics_tool import get_machine_alerts


def build_machine_case(machine_serial_no):

    machine = get_machine_details(machine_serial_no)
    history = get_service_history(machine_serial_no)
    alerts = get_machine_alerts(machine_serial_no)

    return {
        "Machine_Details": machine,
        "Service_History": history,
        "Telematics_Alerts": alerts
    }


# Our Capstone showcase machine
machine_serial = "XYZ20T100388"

case = build_machine_case(machine_serial)

print("\n")
print("=" * 70)
print("AI CAPSTONE - MACHINE CASE")
print("=" * 70)

print("\nMACHINE:")
print(machine_serial)

print("\n--- MACHINE DETAILS ---")
print(case["Machine_Details"])

print("\n--- SERVICE HISTORY ---")

if isinstance(case["Service_History"], str):
    print(case["Service_History"])
else:
    print("Total Service Records:", len(case["Service_History"]))

    for record in case["Service_History"][-5:]:
        print(record)

print("\n--- TELEMATICS ALERTS ---")

if isinstance(case["Telematics_Alerts"], str):
    print(case["Telematics_Alerts"])
else:
    print("Total Alerts:", len(case["Telematics_Alerts"]))

    for alert in case["Telematics_Alerts"][:5]:
        print(alert)

print("\n" + "=" * 70)