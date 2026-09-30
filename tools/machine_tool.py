import pandas as pd

# Load Machine Population dataset
file_path = "data/01_Machine_Population_3200_XYZ20T.xlsx"
machines = pd.read_excel(file_path)


def get_machine_details(machine_serial_no):
    """
    Retrieve details of one machine using its serial number.
    """

    result = machines[
        machines["Machine_Serial_No"].astype(str).str.upper()
        == machine_serial_no.upper()
    ]

    if result.empty:
        return f"Machine {machine_serial_no} not found."

    return result.iloc[0].to_dict()


# Test our tool
machine = get_machine_details("XYZ20T100001")

print("\nMachine Details:")
for key, value in machine.items():
    print(f"{key}: {value}")