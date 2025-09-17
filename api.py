from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
from formulae import calculate_indices, categorize_indices

app = FastAPI(title="Water Quality Analysis API", version="1.0.0")

class WaterSample(BaseModel):
    ParameterName: str
    Ci: float
    Si: float
    Ii: float
    MACi: float

class SampleData(BaseModel):
    SampleID: int
    parameters: List[WaterSample]

class AnalysisResult(BaseModel):
    SampleID: int
    HPI: Optional[float]
    HPI_Category: str
    HEI: Optional[float]
    HEI_Category: str
    Cd: Optional[float]
    Cd_Category: str
    OverallConclusion: str

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_water_sample(sample_data: SampleData):
    try:
        # Convert to DataFrame
        df = pd.DataFrame([param.dict() for param in sample_data.parameters])
        
        # Calculate indices
        HPI, HEI, Cd = calculate_indices(df)
        
        # Categorize indices
        hpi_cat, hei_cat, cd_cat, conclusion = categorize_indices(HPI, HEI, Cd)
        
        return AnalysisResult(
            SampleID=sample_data.SampleID,
            HPI=None if pd.isna(HPI) else round(float(HPI), 2),
            HPI_Category=hpi_cat,
            HEI=None if pd.isna(HEI) else round(float(HEI), 2),
            HEI_Category=hei_cat,
            Cd=None if pd.isna(Cd) else round(float(Cd), 2),
            Cd_Category=cd_cat,
            OverallConclusion=conclusion
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/analyze-batch", response_model=List[AnalysisResult])
async def analyze_batch_samples(samples: List[SampleData]):
    results = []
    for sample in samples:
        try:
            result = await analyze_water_sample(sample)
            results.append(result)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing sample {sample.SampleID}: {str(e)}")
    return results

@app.get("/")
async def root():
    return {"message": "Water Quality Analysis API"}