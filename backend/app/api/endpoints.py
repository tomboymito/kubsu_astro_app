from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from typing import Optional, Literal, Dict, Any
from app.core.services.file_parser import parse_file
from app.core.calculations import (
    sublimation,
    mass,
    nucleus,
)
import json
import logging


router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Astronomy Comet Analysis API is running"}


@router.get("")
async def api_root():
    return {"message": "Welcome to the API root"}


logger = logging.getLogger(__name__)


class CalculationRequest(BaseModel):
    calculation_type: Literal["sublimation", "mass", "nucleus"]
    parameters: Dict[str, Any]
    file_data: Optional[Dict] = None


@router.post("/calculate")
async def calculate_comet_data(
    file: Optional[UploadFile] = File(None),
    calculation_type: str = Form(...),
    parameters: Optional[str] = Form(None),
):
    try:
        # Parse parameters JSON string to dict if provided
        params_dict = {}
        if parameters:
            try:
                params_dict = json.loads(parameters)
            except json.JSONDecodeError as e:
                raise HTTPException(
                    status_code=400, detail=f"Invalid parameters JSON: {str(e)}"
                )

        # Parse file if provided
        file_data = None
        if file:
            file_data = await parse_file(file)

        # Validate request data using CalculationRequest model
        try:
            request_data = CalculationRequest(
                calculation_type=calculation_type,
                parameters=params_dict,
                file_data=file_data,
            )
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=e.errors())

        # Perform calculation based on type
        if request_data.calculation_type == "sublimation":
            result = sublimation.calculate(
                request_data.file_data, request_data.parameters
            )
        elif request_data.calculation_type == "mass":
            result = mass.calculate(request_data.file_data, request_data.parameters)
        elif request_data.calculation_type == "nucleus":
            result = nucleus.calculate(
                request_data.file_data, request_data.parameters
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid calculation type")

        return JSONResponse(
            content={
                "result": result.get("value"),
                "units": result.get(
                    "units", ""
                ),
                "error": None,
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Calculation error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

# @router.get("/plot_data")
# async def get_plot_data(dataset_id: str):
#     try:
#         data = plots.generate_plot_data(dataset_id)
#         return JSONResponse(content={
#             "x": data["x"],
#             "y": data["y"],
#             "labels": data.get("labels", {})
#         })
#     except Exception as e:
#         logger.error(f"Plot data error: {str(e)}", exc_info=True)
#         raise HTTPException(status_code=500, detail="Internal server error")
