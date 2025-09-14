# DeepChem Integration Documentation

## Overview
This module integrates DeepChem property prediction into the core engine using SMILES input from the ZINC250k dataset.

## Steps
1. **Install dependencies**
   - `pip install deepchem pandas requests`
2. **Download ZINC250k dataset**
   - The code automatically downloads the dataset as `zinc_250k.csv`.
3. **Load SMILES strings**
   - Uses pandas to read SMILES from the dataset.
4. **Predict properties**
   - For each molecule, 10 properties are predicted (using placeholder functions; replace with actual DeepChem models as needed).
5. **Run predictions**
   - Run `main.py` to execute the workflow and print results for the first 10 molecules.

## Output Example
```
{
  "smiles": "CCO",
  "toxicity": 0.5,
  "solubility": -2.0,
  "bioactivity": true,
  "permeability": 0.7,
  "logP": 1.2,
  "stability": "medium",
  "binding_affinity": 6.5,
  "mutagenicity": false,
  "toxicological_endpoints": {"LC50": 100, "IC50": 20},
  "custom_hmpi": 0.8
}
```

## Customization
- Replace the placeholder prediction functions in `deepchem_integration.py` with actual DeepChem model calls for each property.
- Integrate with API or other modules as needed.

## References
- DeepChem documentation: https://deepchem.io/
- ZINC dataset: https://zinc.docking.org/
