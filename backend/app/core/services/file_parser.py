from fastapi import UploadFile, HTTPException
from astropy.io import fits
import numpy as np
import pandas as pd
from typing import Dict, Union
import logging
import tempfile
from io import StringIO

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def parse_txt(file_content: str) -> Dict[str, np.ndarray]:
    """Парсит текстовый файл с данными кометы"""
    try:
        # Чтение данных через StringIO
        data = pd.read_csv(StringIO(file_content), delim_whitespace=True, comment='#')
        
        # Проверка на пустые данные
        if data.empty:
            raise ValueError("File contains no data")

        # Проверка обязательных колонок
        required_columns = {
            "Дни_до_перигелия": "days_to_perihelion",
            "Звёздная_величина": "magnitude",
            "Afrho": "afrho"
        }

        missing_cols = [col for col in required_columns if col not in data.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")

        # Конвертация данных
        return {
            "days_to_perihelion": data["Дни_до_перигелия"].values.astype(float),
            "magnitude": data["Звёздная_величина"].values.astype(float),
            "afrho": data["Afrho"].values.astype(float)
        }
    except Exception as e:
        logger.error(f"Error parsing TXT file: {str(e)}")
        raise ValueError(f"TXT file parsing error: {str(e)}")

def parse_fits(file_path: str) -> Dict[str, np.ndarray]:
    """Парсит FITS файл с данными кометы"""
    try:
        with fits.open(file_path) as hdul:
            if len(hdul) < 2:
                raise ValueError("FITS file must contain at least 2 HDUs")

            data = hdul[1].data
            
            # Проверка обязательных полей
            required_fields = ["Days_to_Perihelion", "Magnitude", "Afrho"]
            missing_fields = [field for field in required_fields if field not in data.names]
            
            if missing_fields:
                raise ValueError(f"Missing required fields in FITS: {', '.join(missing_fields)}")

            return {
                "days_to_perihelion": data["Days_to_Perihelion"].astype(float),
                "magnitude": data["Magnitude"].astype(float),
                "afrho": data["Afrho"].astype(float)
            }
    except Exception as e:
        logger.error(f"Error parsing FITS file: {str(e)}")
        raise ValueError(f"FITS file parsing error: {str(e)}")

async def parse_file(file: UploadFile) -> Dict[str, Union[np.ndarray, list]]:
    """Основная функция парсинга файлов"""
    try:
        # Проверка размера файла
        if file.size > MAX_FILE_SIZE:
            raise ValueError(f"File size exceeds maximum limit of {MAX_FILE_SIZE//(1024*1024)} MB")

        content = await file.read()
        
        if not content:
            raise ValueError("Uploaded file is empty")

        # Определение типа файла и парсинг
        if file.filename.endswith('.txt'):
            return parse_txt(content.decode('utf-8'))
        elif file.filename.endswith('.fits'):
            with tempfile.NamedTemporaryFile(delete=True) as tmp:
                tmp.write(content)
                tmp.flush()
                return parse_fits(tmp.name)
        else:
            raise ValueError(
                f"Unsupported file format: {file.filename.split('.')[-1]}. "
                "Supported formats: .txt, .fits"
            )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"File parsing failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error during file parsing"
        )