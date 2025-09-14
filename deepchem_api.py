from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import traceback

import deepchem_integration as dci

app = FastAPI(title="DeepChem Property Prediction API", description="API for molecular property prediction using SMILES and ZINC dataset.")

class SmilesRequest(BaseModel):
    smiles: str

@app.get("/load_smiles", response_model=List[str])
def load_smiles():
    """Load all SMILES from the local ZINC dataset."""
    try:
        return dci.load_smiles()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/get_all_properties")
def get_all_properties(req: SmilesRequest):
    """Get all properties for a given SMILES string."""
    try:
        return dci.get_all_properties(req.smiles)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_toxicity")
def predict_toxicity(req: SmilesRequest):
    try:
        return {"toxicity": dci.predict_toxicity(req.smiles)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_solubility")
def predict_solubility(req: SmilesRequest):
    try:
        return {"solubility": dci.predict_solubility(req.smiles)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_bioactivity")
def predict_bioactivity(req: SmilesRequest):
    try:
        return {"bioactivity": dci.predict_bioactivity(req.smiles)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_permeability")
def predict_permeability(req: SmilesRequest):
    try:
        return {"permeability": dci.predict_permeability(req.smiles)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_logP")
def predict_logP(req: SmilesRequest):
    try:
        return {"logP": dci.predict_logP(req.smiles)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_stability")
def predict_stability(req: SmilesRequest):
    try:
        return {"stability": dci.predict_stability(req.smiles)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_binding_affinity")
def predict_binding_affinity(req: SmilesRequest):
    try:
        return {"binding_affinity": dci.predict_binding_affinity(req.smiles)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_mutagenicity")
def predict_mutagenicity(req: SmilesRequest):
    try:
        return {"mutagenicity": dci.predict_mutagenicity(req.smiles)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_toxicological_endpoints")
def predict_toxicological_endpoints(req: SmilesRequest):
    try:
        return {"toxicological_endpoints": dci.predict_toxicological_endpoints(req.smiles)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_custom_hmpi")
def predict_custom_hmpi(req: SmilesRequest):
    try:
        return {"custom_hmpi": dci.predict_custom_hmpi(req.smiles)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/properties_list", response_model=List[str])
def properties_list():
    """Get the list of all available property names."""
    return dci.PROPERTIES


class BulkSmilesRequest(BaseModel):
    smiles_list: List[str]

@app.post("/bulk_get_all_properties")
def bulk_get_all_properties(req: BulkSmilesRequest):
    """
    Get all properties for a list of SMILES strings.
    """
    results = []
    for smiles in req.smiles_list:
        try:
            result = dci.get_all_properties(smiles)
        except Exception as e:
            result = {"smiles": smiles, "error": str(e)}
        results.append(result)
    return results

@app.post("/bulk_predict_toxicity")
def bulk_predict_toxicity(req: BulkSmilesRequest):
    """
    Predict toxicity for a list of SMILES strings.
    """
    results = []
    for smiles in req.smiles_list:
        try:
            value = dci.predict_toxicity(smiles)
        except Exception as e:
            value = str(e)
        results.append({"smiles": smiles, "toxicity": value})
    return results

@app.post("/bulk_predict_solubility")
def bulk_predict_solubility(req: BulkSmilesRequest):
    results = []
    for smiles in req.smiles_list:
        try:
            value = dci.predict_solubility(smiles)
        except Exception as e:
            value = str(e)
        results.append({"smiles": smiles, "solubility": value})
    return results

@app.post("/bulk_predict_bioactivity")
def bulk_predict_bioactivity(req: BulkSmilesRequest):
    results = []
    for smiles in req.smiles_list:
        try:
            value = dci.predict_bioactivity(smiles)
        except Exception as e:
            value = str(e)
        results.append({"smiles": smiles, "bioactivity": value})
    return results

@app.post("/bulk_predict_permeability")
def bulk_predict_permeability(req: BulkSmilesRequest):
    results = []
    for smiles in req.smiles_list:
        try:
            value = dci.predict_permeability(smiles)
        except Exception as e:
            value = str(e)
        results.append({"smiles": smiles, "permeability": value})
    return results

@app.post("/bulk_predict_logP")
def bulk_predict_logP(req: BulkSmilesRequest):
    results = []
    for smiles in req.smiles_list:
        try:
            value = dci.predict_logP(smiles)
        except Exception as e:
            value = str(e)
        results.append({"smiles": smiles, "logP": value})
    return results

@app.post("/bulk_predict_stability")
def bulk_predict_stability(req: BulkSmilesRequest):
    results = []
    for smiles in req.smiles_list:
        try:
            value = dci.predict_stability(smiles)
        except Exception as e:
            value = str(e)
        results.append({"smiles": smiles, "stability": value})
    return results

@app.post("/bulk_predict_binding_affinity")
def bulk_predict_binding_affinity(req: BulkSmilesRequest):
    results = []
    for smiles in req.smiles_list:
        try:
            value = dci.predict_binding_affinity(smiles)
        except Exception as e:
            value = str(e)
        results.append({"smiles": smiles, "binding_affinity": value})
    return results

@app.post("/bulk_predict_mutagenicity")
def bulk_predict_mutagenicity(req: BulkSmilesRequest):
    results = []
    for smiles in req.smiles_list:
        try:
            value = dci.predict_mutagenicity(smiles)
        except Exception as e:
            value = str(e)
        results.append({"smiles": smiles, "mutagenicity": value})
    return results

@app.post("/bulk_predict_toxicological_endpoints")
def bulk_predict_toxicological_endpoints(req: BulkSmilesRequest):
    results = []
    for smiles in req.smiles_list:
        try:
            value = dci.predict_toxicological_endpoints(smiles)
        except Exception as e:
            value = str(e)
        results.append({"smiles": smiles, "toxicological_endpoints": value})
    return results

@app.post("/bulk_predict_custom_hmpi")
def bulk_predict_custom_hmpi(req: BulkSmilesRequest):
    results = []
    for smiles in req.smiles_list:
        try:
            value = dci.predict_custom_hmpi(smiles)
        except Exception as e:
            value = str(e)
        results.append({"smiles": smiles, "custom_hmpi": value})
    return results