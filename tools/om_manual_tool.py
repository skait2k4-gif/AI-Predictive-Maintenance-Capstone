import pandas as pd

file_path = "data/05_Synthetic_Operation_Maintenance_Manual_XYZ20T.xlsx"

om_manual = pd.read_excel(file_path)


def search_om_manual(search_term):
    """
    Retrieve approved Operation & Maintenance guidance
    relevant to the requested topic.
    """

    result = om_manual[
        (
            om_manual["Topic"]
            .astype(str)
            .str.contains(search_term, case=False, na=False)
        )
        &
        (
            om_manual["Approval_Status"]
            .astype(str)
            .str.upper()
            == "APPROVED"
        )
    ]

    if result.empty:
        return f"No approved O&M guidance found for {search_term}"

    return result.to_dict(orient="records")


# Test for our cooling-system case

search_term = "Cooling"

guidance = search_om_manual(search_term)

print("\n===== OPERATION & MAINTENANCE KNOWLEDGE =====")
print("Search Topic:", search_term)

if isinstance(guidance, str):
    print(guidance)

else:
    print("Relevant Approved Sections:", len(guidance))

    for item in guidance:

        print("\n----------------------------------")

        print("Document:", item.get("Doc_ID"))
        print("Section:", item.get("Section_ID"))
        print("Topic:", item.get("Topic"))

        print(
            "Guidance:",
            item.get("Operating_or_Maintenance_Guidance")
        )

        print(
            "Inspection / Action:",
            item.get("Inspection_or_Action")
        )

        print(
            "Interval / Trigger:",
            item.get("Interval_or_Trigger")
        )

        print(
            "Warning / Limitation:",
            item.get("Warning_or_Limitation")
        )