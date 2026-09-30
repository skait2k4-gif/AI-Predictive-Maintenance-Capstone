import pandas as pd

file_path = "data/04_Synthetic_Troubleshooting_Manual_XYZ20T.xlsx"

manual = pd.read_excel(file_path)


def search_troubleshooting(system_name):
    """
    Retrieve approved troubleshooting knowledge
    relevant to a machine system.
    """

    result = manual[
        (
            manual["System"]
            .astype(str)
            .str.contains(system_name, case=False, na=False)
        )
        &
        (
            manual["Approval_Status"]
            .astype(str)
            .str.upper()
            == "APPROVED"
        )
    ]

    if result.empty:
        return f"No approved troubleshooting guidance found for {system_name}"

    return result.to_dict(orient="records")


# Test with our showcase cooling-system case

system = "Cooling"

guidance = search_troubleshooting(system)

print("\n===== TROUBLESHOOTING KNOWLEDGE =====")
print("System:", system)

if isinstance(guidance, str):
    print(guidance)

else:
    print("Relevant Approved Sections:", len(guidance))

    for item in guidance:
        print("\n----------------------------------")

        print("Document:", item.get("Doc_ID"))
        print("Section:", item.get("Section_ID"))
        print("Symptom / Alert:", item.get("Symptom_or_Alert"))
        print("Possible Cause:", item.get("Possible_Cause"))
        print("Inspection:", item.get("Inspection_Sequence"))
        print("Recommended Action:", item.get("Recommended_Action"))
        print("Escalation:", item.get("Escalation_Criteria"))
        print("Safety / HITL:", item.get("Safety_HITL_Note"))