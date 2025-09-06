# === formulae registry ===
import pandas as pd

def calculate_indices(df):
    df["Qi"] = ((df["Ci"] - df["Ii"]) / (df["Si"] - df["Ii"])) * 100  
    df["Wi"] = (1 / df["Si"]) / (1 / df["Si"]).sum()
    df["Cfi"] = df["Ci"] / df["Si"]

    HPI = (df["Qi"] * df["Wi"]).sum() / df["Wi"].sum()
    HEI = (df["Ci"] / df["MACi"]).sum()
    Cd = (df["Cfi"] - 1).sum()

    return HPI, HEI, Cd




// all heavy metal(45, 60), thier organic, chemical, pyhsical reqctions as same as real world (1k+) 
// mole of every reaction, chained reactions
// as -> aso2 -> pbo2 => aso2 pb02 > phyiccal, impllications 
// csv excel 
// csv -> json -> json -> csv 
// BULK routes expose -> microservice archietecutre
// impacts and thier description of equations 
// humidity, turbidty, temperature  ETC
// date ->   10 
// not harcoded -> formula registry
// FORMULA REGISTRY MULTUABLE 
// UNITS FRONTENDS MUTABLE // ROUTE (PARAMETERS MG/L, DATA INCOMPLTE(25 ELEMENTS ))
# the actual code that shows the possible reactions when x y z heave metals are present - anshita
# output should be json -Devansh
# mole of reactions fomrula and code - Raghav
# list of chemical reactions - kunal
