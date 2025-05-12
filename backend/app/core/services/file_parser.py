from fastapi import UploadFile
from astropy.io import fits
import numpy as np
import pandas as pd
from typing import Dict, Union
import logging


logger = logging.getLogger(__name__)


def parse_txt(file_content: str) -> Dict[str, np.ndarray]:
    try:
        data = pd.read_csv(file_content, delim_whitespace=True)
        required_columns = ["Дни_до_перигелия", "Звёздная_величина", "Afrho"]

        if not all(col in data.columns for col in required_columns):
            raise ValueError("Missing required columns in TXT file")

        return {
            "days_to_perihelion": data["Дни_до_перигелия"].values,
            "magnitude": data["Звёздная_величина"].values,
            "afrho": data["Afrho"].values
        }
    except Exception as e:
        logger.error(f"Error parsing TXT file: {str(e)}")
        raise


def parse_fits(file_path: str) -> Dict[str, np.ndarray]:
    try:
        with fits.open(file_path) as hdul:
            data = hdul[1].data

        return {
            "days_to_perihelion": data["Days_to_Perihelion"],
            "magnitude": data["Magnitude"],
            "afrho": data["Afrho"]
        }
    except Exception as e:
        logger.error(f"Error parsing FITS file: {str(e)}")
        raise


async def parse_file(file: UploadFile) -> Dict[str, Union[np.ndarray, list]]:
    try:
        content = await file.read()

        if file.filename.endswith('.txt'):
            return parse_txt(content.decode('utf-8'))
        if file.filename.endswith('.fits'):
            # Для FITS файлов нужно сохранить временный файл
            import tempfile
            with tempfile.NamedTemporaryFile(delete=True) as tmp:
                tmp.write(content)
                tmp.flush()
                # Возвращаем результат парсинга временного файла
                return parse_fits(tmp.name)
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        logger.error(f"File parsing failed: {str(e)}")
        raise
