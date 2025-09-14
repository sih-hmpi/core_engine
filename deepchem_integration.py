"""
Module to handle property predictions for molecules using SMILES input (RDKit + precomputed CSV).
"""
import pandas as pd
import requests
import csv
from rdkit import Chem
from rdkit.Chem import Crippen, Descriptors, Lipinski, QED

ZINC_URL = "https://raw.githubusercontent.com/aspuru-guzik-group/chemical_vae/master/data/zinc_250k.csv"
ZINC_LOCAL = "zinc_250k.csv"  # Update path if needed

PROPERTIES = [
    "toxicity",
    "solubility",
    "bioactivity",
    "permeability",
    "logP",
    "stability",
    "binding_affinity",
    "mutagenicity",
    "toxicological_endpoints",
    "custom_hmpi"
]


import os
def load_smiles():
    """
    Loads SMILES from local ZINC dataset. If not present, does NOT download, just raises error.
    Returns list of cleaned SMILES strings.
    """
    if not os.path.exists(ZINC_LOCAL):
        raise FileNotFoundError(f"Dataset not found at {ZINC_LOCAL}. Please download manually.")
    df = pd.read_csv(ZINC_LOCAL, quoting=csv.QUOTE_ALL, engine='python', skip_blank_lines=True)
    df.columns = df.columns.str.strip().str.replace('"', '')
    if 'smiles' not in df.columns:
        raise Exception(f"'smiles' column not found! Columns are: {df.columns.tolist()}")
    df['smiles'] = df['smiles'].astype(str).str.replace('"', '').str.replace('\n', '').str.strip()
    return df['smiles'].dropna().tolist()

def get_precomputed_row(smiles):
    """
    Returns the row from the local ZINC dataset matching the cleaned SMILES string, or None if not found.
    """
    if not os.path.exists(ZINC_LOCAL):
        return None
    df = pd.read_csv(ZINC_LOCAL, quoting=csv.QUOTE_ALL, engine='python', skip_blank_lines=True)
    df.columns = df.columns.str.strip().str.replace('"', '')
    df['smiles'] = df['smiles'].astype(str).str.replace('"', '').str.replace('\n', '').str.strip()
    smiles_clean = smiles.strip().replace('\n', '').replace('"', '')
    row = df[df['smiles'] == smiles_clean]
    if not row.empty:
        return row.iloc[0]
    return None

def predict_toxicity(smiles):
    row = get_precomputed_row(smiles)
    if row is not None and 'qed' in row:
        qed = row['qed']
    else:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        qed = QED.qed(mol)
    return 1.0 - float(qed)

def predict_solubility(smiles):
    row = get_precomputed_row(smiles)
    if row is not None and 'SAS' in row:
        sas = row['SAS']
        return -float(sas)
    else:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        mw = Descriptors.MolWt(mol)
        return -mw / 100.0

def predict_bioactivity(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    donors = Lipinski.NumHDonors(mol)
    return donors > 1

def predict_permeability(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    rot_bonds = Lipinski.NumRotatableBonds(mol)
    return max(0, 1 - rot_bonds / 10.0)

def predict_logP(smiles):
    row = get_precomputed_row(smiles)
    if row is not None and 'logP' in row:
        return float(row['logP'])
    else:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        return Crippen.MolLogP(mol)

def predict_stability(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    rings = mol.GetRingInfo().NumRings()
    if rings == 0:
        return "low"
    elif rings < 3:
        return "medium"
    else:
        return "high"

def predict_binding_affinity(smiles):
    row = get_precomputed_row(smiles)
    if row is not None and 'qed' in row:
        return float(row['qed'])
    else:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        return QED.qed(mol)

def predict_mutagenicity(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    n_atoms = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'N')
    return n_atoms > 2

def predict_toxicological_endpoints(smiles):
    return None

def predict_custom_hmpi(smiles):
    logp = predict_logP(smiles)
    sol = predict_solubility(smiles)
    row = get_precomputed_row(smiles)
    if row is not None and 'qed' in row:
        qed = float(row['qed'])
    else:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        qed = QED.qed(mol)
    if None in (logp, sol, qed):
        return None
    return (logp + sol + qed) / 3.0

def get_all_properties(smiles):
    return {
        "smiles": smiles,
        "toxicity": predict_toxicity(smiles),
        "solubility": predict_solubility(smiles),
        "bioactivity": predict_bioactivity(smiles),
        "permeability": predict_permeability(smiles),
        "logP": predict_logP(smiles),
        "stability": predict_stability(smiles),
        "binding_affinity": predict_binding_affinity(smiles),
        "mutagenicity": predict_mutagenicity(smiles),
        "toxicological_endpoints": predict_toxicological_endpoints(smiles),
        "custom_hmpi": predict_custom_hmpi(smiles)
    }