from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from typing import Optional, Literal, Dict, Any
from backend.app.core.services.file_parser import parse_file
from backend.app.core.calculations import (
    sublimation,
    mass,
    nucleus,
)
import json
import logging

router = APIRouter(
    prefix="/api",
    tags=["calculations"],
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)

class CalculationRequest(BaseModel):
    """Схема запроса для расчетов"""
    calculation_type: Literal["sublimation", "mass", "nucleus"]
    parameters: Dict[str, Any]
    file_data: Optional[Dict] = None

class PlotDataResponse(BaseModel):
    x: list
    y: list
    labels: Optional[Dict[str, Any]] = None

@router.post("/calculate",
             summary="Выполнить астрономический расчет",
             response_description="Результаты расчета")
async def calculate_comet_data(
    file: Optional[UploadFile] = File(None),
    calculation_type: str = Form(...),
    parameters: Optional[str] = Form(None),
):
    """Выполняет астрономические расчеты"""
    try:
        if not file and not parameters:
            raise HTTPException(
                status_code=400,
                detail="Either file or parameters must be provided"
            )

        params_dict = {}
        if parameters:
            try:
                params_dict = json.loads(parameters)
                if not isinstance(params_dict, dict):
                    raise ValueError("Parameters must be a JSON object")
            except json.JSONDecodeError as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid parameters JSON: {str(e)}"
                )

        file_data = None
        if file:
            if not file.filename:
                raise HTTPException(
                    status_code=400,
                    detail="Uploaded file must have a filename"
                )
            file_data = await parse_file(file)

        try:
            request_data = CalculationRequest(
                calculation_type=calculation_type,
                parameters=params_dict,
                file_data=file_data,
            )
        except ValidationError as e:
            raise HTTPException(
                status_code=422,
                detail=e.errors()
            )

        try:
            if request_data.calculation_type == "sublimation":
                result = sublimation.calculate(
                    request_data.file_data, request_data.parameters
                )
            elif request_data.calculation_type == "mass":
                result = mass.calculate(
                    request_data.file_data, request_data.parameters
                )
            elif request_data.calculation_type == "nucleus":
                result = nucleus.calculate(
                    request_data.file_data, request_data.parameters
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid calculation type"
                )

            return JSONResponse(
                content={
                    "result": result.get("value"),
                    "units": result.get("units", ""),
                    "error": None,
                }
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Calculation error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

@router.get("/plot_data",
            summary="Получить данные для графиков",
            response_model=PlotDataResponse)
async def get_plot_data(dataset_id: str):
    """Возвращает данные для построения графиков"""
    try:
        # Здесь должна быть реальная логика получения данных
        return {
            "x": [1, 2, 3, 4, 5],
            "y": [10, 20, 15, 25, 30],
            "labels": {"x": "Days", "y": "Magnitude"}
        }
    except Exception as e:
        logger.error(f"Failed to get plot data: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")