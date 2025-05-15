from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError  # Добавлен импорт BaseModel
from typing import Optional, Literal, Dict, Any
from application.backend.app.core.services.file_parser import parse_file  # Обновленный импорт
from application.backend.app.core.calculations import (
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

class CalculationResponse(BaseModel):
    """Схема ответа с результатами расчета"""
    result: Any
    units: Optional[str] = None
    error: Optional[str] = None

@router.post("/calculate",
             summary="Выполнить астрономический расчет",
             response_model=CalculationResponse)
async def calculate_comet_data(
    file: Optional[UploadFile] = File(None),
    calculation_type: str = Form(...),
    parameters: Optional[str] = Form(None),
):
    """Выполняет один из доступных астрономических расчетов"""
    try:
        # Проверка наличия входных данных
        if not file and not parameters:
            raise HTTPException(
                status_code=400,
                detail="Either file or parameters must be provided"
            )

        # Парсинг параметров
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

        # Парсинг файла
        file_data = None
        if file:
            if not file.filename:
                raise HTTPException(
                    status_code=400,
                    detail="Uploaded file must have a filename"
                )
            file_data = await parse_file(file)

        # Валидация запроса
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

        # Выполнение расчета
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

            return {
                "result": result.get("value"),
                "units": result.get("units", ""),
                "error": None,
            }
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