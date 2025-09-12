import pandas as pd
from formulae import calculate_indices, categorize_indices

# === Sample dataset ===
data = {
    "SampleID": [1, 2],
    "ParameterName": [["Lead", "Cadmium", "Arsenic"], ["Lead", "Cadmium", "Arsenic"]],
    "Ci": [[0.15, 0.01, 0.02], [0.05, 0.005, 0.01]],
    "Si": [[0.05, 0.003, 0.01], [0.05, 0.003, 0.01]],
    "Ii": [[0, 0, 0], [0, 0, 0]],
    "MACi": [[0.05, 0.003, 0.01], [0.05, 0.003, 0.01]]
}
df = pd.DataFrame(data)

# === Process each sample and display results ===
for idx, row in df.iterrows():
    sample_df = pd.DataFrame({
        "ParameterName": row["ParameterName"],
        "Ci": row["Ci"],
        "Si": row["Si"],
        "Ii": row["Ii"],
        "MACi": row["MACi"]
    })

    # Calculate indices
    HPI, HEI, Cd = calculate_indices(sample_df)

    # Categorize indices
    hpi_cat, hei_cat, cd_cat, conclusion = categorize_indices(HPI, HEI, Cd)

    print(f"SampleID: {row['SampleID']}")
    print(f"HPI: {HPI:.2f} -> {hpi_cat}")
    print(f"HEI: {HEI:.2f} -> {hei_cat}")
    print(f"Cd: {Cd:.2f} -> {cd_cat}")
    print(f"Overall Conclusion: {conclusion}")
    print("-" * 50)
