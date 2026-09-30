import pandas as pd

file_path = "data/02_Machine_Service_History_Integrated.xlsx"

service_history = pd.read_excel(
    file_path,
    sheet_name="Machine Service History"
)


def get_service_history(machine_serial_no):
    """
    Retrieve the complete service history
    for a particular machine.
    """

    result = service_history[
        service_history["Machine_Serial_No"]
        .astype(str)
        .str.upper()
        == machine_serial_no.upper()
    ]

    if result.empty:
        return f"No service history found for {machine_serial_no}"

    return result.to_dict(orient="records")


# Test the tool
machine_serial = "XYZ20T100001"

history = get_service_history(machine_serial)

print(f"\nSERVICE HISTORY FOR: {machine_serial}")
print("=" * 60)

if isinstance(history, str):
    print(history)

else:
    print("Total Service Records:", len(history))

    for record in history:
        print("\n----------------------------")

        for key, value in record.items():
            print(f"{key}: {value}")