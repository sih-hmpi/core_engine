def calculate_indices(df):
    
    # === Step 1: Calculate sub-indices ===
 
    # Qi = Sub-index of ith metal
    # Measures how much the current concentration Ci deviates from the ideal value Ii
    # Si is the standard permissible value for that metal
    # Formula: Qi = ((Ci - Ii) / (Si - Ii)) * 100
    
    df["Qi"] = ((df["Ci"] - df["Ii"]) / (df["Si"] - df["Ii"])) * 100  

    # Wi = Weight of the nth metal
    # Higher weight for metals with lower permissible limits (more toxic)
    # Formula: Wi = (1/Si) / sum(1/Si for all metals)
    
    df["Wi"] = (1 / df["Si"]) / (1 / df["Si"]).sum()

    # Cfi = Contamination factor for ith metal
    # Ratio of measured concentration to standard
    
    df["Cfi"] = df["Ci"] / df["Si"]

    # === Step 2: Calculate Indices ===

    # HPI (Heavy Metal Pollution Index)
    # Weighted average of sub-indices Qi
    # Interpretation:
    # HPI < 50: Low/acceptable pollution
    # 50 <= HPI <100 : Moderate pollution
    # 100 <= HPI <200: High pollution
    # HPI >= 200: Very high pollution
    
    HPI = (df["Qi"] * df["Wi"]).sum() / df["Wi"].sum()

    # HEI (Heavy Metal Evaluation Index)
    # Sum of ratios of concentration to maximum allowable concentration (MACi)
    # Interpretation:
    # HEI < 10: Low risk
    # 10 <= HEI <20 : Medium risk
    # 20 <= HEI <50 : High risk
    # HEI >= 50: Very high risk
    
    HEI = (df["Ci"] / df["MACi"]).sum()

    # Cd (Contamination Degree)
    # Sum of contamination factors minus 1
    # Shows overall contamination above permissible limits
    # Interpretation:
    # Cd < 1: Low contamination
    # 1 <= Cd < 3 : Moderate contamination
    # 3 <= Cd < 6 : High contamination
    # Cd >= 6: Very high contamination
    
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

