from pydantic import BaseModel
from typing import Optional, Dict, Any, Literal


class CalculationRequest(BaseModel):
    calculation_type: Literal["sublimation", "mass", "nucleus"]
    parameters: Dict[str, Any]
    file_data: Optional[Dict] = None


class CalculationResponse(BaseModel):
    result: Any
    units: Optional[str] = None
    error: Optional[str] = None


class PlotDataResponse(BaseModel):
    x: list
    y: list
    labels: Optional[Dict[str, Any]] = None
