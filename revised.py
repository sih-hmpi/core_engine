import pandas as pd
import json
from formula1 import calculate_indices, categorize_indices

data = {
    "SampleID": [1, 1, 1, 1, 1,
                 2, 2, 2, 2, 2,
                 3, 3, 3, 3, 3],
    "ParameterName": ["pH", "Lead", "Iron", "Nitrate", "Chloride",
                      "pH", "Lead", "Iron", "Nitrate", "Chloride",
                      "pH", "Lead", "Iron", "Nitrate", "Chloride"],
    "Ci": [7.2, 0.03, 0.4, 20, 150,
           6.8, 0.07, 0.2, 60, 320,
           7.5, 0.01, 0.1, 10, 90],
    "Si": [8.5, 0.05, 0.3, 45, 250,
           8.5, 0.05, 0.3, 45, 250,
           8.5, 0.05, 0.3, 45, 250],
    "Ii": [7, 0, 0.1, 0, 0,
           7, 0, 0.1, 0, 0,
           7, 0, 0.1, 0, 0],
    "MACi": [9, 0.01, 1.0, 50, 1000,
             9, 0.01, 1.0, 50, 1000,
             9, 0.01, 1.0, 50, 1000]
}

df = pd.DataFrame(data)

for col in ["Ci", "Si", "Ii", "MACi"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

results = []  

# === Process each sample and display results ===
for sample_id, row in df.groupby("SampleID"):
    sample_df = row[["ParameterName", "Ci", "Si", "Ii", "MACi"]]

    # Calculate indices
    HPI, HEI, Cd = calculate_indices(sample_df)

    # Categorize indices
    hpi_cat, hei_cat, cd_cat, conclusion = categorize_indices(HPI, HEI, Cd)

    # Store result
    result = {
        "SampleID": int(sample_id),
        "HPI": None if pd.isna(HPI) else round(float(HPI), 2),
        "HPI_Category": hpi_cat,
        "HEI": None if pd.isna(HEI) else round(float(HEI), 2),
        "HEI_Category": hei_cat,
        "Cd": None if pd.isna(Cd) else round(float(Cd), 2),
        "Cd_Category": cd_cat,
        "OverallConclusion": conclusion
    }

    # Print for quick check
    print(f"SampleID: {sample_id}")
    print(f"HPI: {HPI:.2f} -> {hpi_cat}")
    print(f"HEI: {HEI:.2f} -> {hei_cat}")
    print(f"Cd: {Cd:.2f} -> {cd_cat}")
    print(f"Overall Conclusion: {conclusion}")
    print("-" * 50)

    results.append(result)

# Save results to JSON
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

print("Results saved to output.json")
