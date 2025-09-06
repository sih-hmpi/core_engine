# === main file ===
import pandas as pd
from formulae import calculate_indices
import requests

# Sample data that can be replaced with actual data loading
data = {
    "SampleID": [1, 2],
    "ParameterName": [["Lead", "Cadmium", "Arsenic"], ["Lead", "Cadmium", "Arsenic"]],
    "Ci": [[0.15, 0.01, 0.02], [0.05, 0.005, 0.01]],
    "Si": [[0.05, 0.003, 0.01], [0.05, 0.003, 0.01]],
    "Ii": [[0, 0, 0], [0, 0, 0]],
    "MACi": [[0.05, 0.003, 0.01], [0.05, 0.003, 0.01]]
}


df = pd.DataFrame(data)

API_KEY = "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" 

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "HTTP-Referer": "http://localhost",
    "X-Title": "My App",
}

results_list = []

for idx, row in df.iterrows():
    sample_df = pd.DataFrame({
        "ParameterName": row["ParameterName"],
        "Ci": row["Ci"],
        "Si": row["Si"],
        "Ii": row["Ii"],
        "MACi": row["MACi"]
    })
    
    HPI, HEI, Cd = calculate_indices(sample_df)
    
    data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant specialized in water quality."
        },
        {
            "role": "user",
            "content": (
                f"Interpret these water quality indices: HPI={HPI:.2f}, HEI={HEI:.2f}, Cd={Cd:.2f}. "
                "HPI = Heavy Metal Pollution Index, HEI = Heavy Metal Evaluation Index, Cd = Contamination Index. "
                "For each index, show it as 'value -> category' using the scales:\n\n"
                "\n"
                "HPI: <100 = safe, 100–200 = caution, 200+ = unsafe\n"
                "HEI: <10 = low pollution, 10–20 = medium, 20+ = high\n"
                "Cd: <1 = low, 1–3 = medium, >=3 = high\n\n"
                "\t"
                "\n"
                "Then provide a short 1 line description with a practical recommendation."
            )
        }
    ]
}
    
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    ai_description = response.json()["choices"][0]["message"]["content"]
    
    results_list.append({
        "Component": f"Sample {row['SampleID']}",
        "HPI Value": round(HPI, 3),
        "HEI Value": round(HEI, 3),
        "Cd Value": round(Cd, 3),
        "Description": ai_description
    })

results_df = pd.DataFrame(results_list)

results_df["HPI Value"] = results_df["HPI Value"].astype(float)
results_df["HEI Value"] = results_df["HEI Value"].astype(float)
results_df["Cd Value"] = results_df["Cd Value"].astype(float)

results_df.to_csv("water_quality_results.csv", index=False)
results_df.to_excel("water_quality_results.xlsx", index=False)
print("Results saved to water_quality_results.csv and water_quality_results.xlsx")



