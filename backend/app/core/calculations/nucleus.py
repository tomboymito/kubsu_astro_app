import numpy as np
from math import sqrt, pi
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def calculate_diameter(A: float, p: float, H: float) -> float:
    """Расчет диаметра ядра кометы по формуле: D = sqrt(4*A / (π*p*H))"""
    try:
        if p <= 0 or H <= 0:
            raise ValueError("Albedo (p) and absolute magnitude (H) must be positive")
            
        diameter = sqrt(4 * A / (pi * p * H))
        return diameter
    except Exception as e:
        logger.error(f"Error in nucleus diameter calculation: {str(e)}")
        raise

def calculate(file_data: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Основная функция расчета размера ядра кометы"""
    try:
        # Проверка наличия необходимых параметров
        if "A" not in parameters:
            raise ValueError("Missing parameter 'A' (projected area)")
        
        # Параметры по умолчанию
        default_params = {
            "p": 0.04,  # Альбедо (типичное значение для комет)
            "H": 18.0   # Абсолютная звездная величина
        }
        
        # Обновление параметров пользовательскими значениями
        params = {**default_params, **parameters}
        
        # Расчет диаметра
        diameter = calculate_diameter(parameters["A"], params["p"], params["H"])
        
        return {
            "value": diameter,
            "units": "km",
            "albedo": params["p"]
        }
    except Exception as e:
        logger.error(f"Nucleus diameter calculation failed: {str(e)}")
        raise