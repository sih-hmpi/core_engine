# === formulae registry ===
import pandas as pd

def calculate_indices(df):
    # Always work on a copy
    df = df.copy()

    # Ensure numeric conversion
    for col in ["Ci", "Si", "Ii", "MACi"]:
        df.loc[:, col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows where Si <= 0 or missing
    df = df[df["Si"] > 0].copy()

    if df.empty:
        return float("nan"), 0.0, 0.0   # no valid data

    # Qi
    df["Qi"] = ((df["Ci"] - df["Ii"]) / (df["Si"] - df["Ii"])) * 100

    # Wi
    denom = (1 / df["Si"]).sum()
    if denom == 0:
        return float("nan"), 0.0, 0.0

    df["Wi"] = (1 / df["Si"]) / denom

    # Indices
    HPI = (df["Qi"] * df["Wi"]).sum() / df["Wi"].sum()
    HEI = (df["Ci"] / df["Si"]).sum()
    Cd = (df["Ci"] / df["MACi"]).sum()

    return HPI, HEI, Cd

def categorize_indices(HPI, HEI, Cd):
    # HPI
    if HPI < 100:
        hpi_cat = "safe"
    elif HPI < 200:
        hpi_cat = "caution"
    else:
        hpi_cat = "unsafe"

    # HEI
    if HEI < 10:
        hei_cat = "low pollution"
    elif HEI < 20:
        hei_cat = "medium"
    else:
        hei_cat = "high"

    # Cd
    if Cd < 1:
        cd_cat = "low contamination"
    elif Cd < 3:
        cd_cat = "medium"
    else:
        cd_cat = "high"

    # Precise conclusion
    if hpi_cat == "unsafe" or cd_cat == "high":
        conclusion = "Unsafe"
    elif hpi_cat == "caution" or cd_cat == "medium":
        conclusion = "Moderate / Caution"
    else:
        conclusion = "Safe"

    return hpi_cat, hei_cat, cd_cat, conclusion

