import ctypes
import logging
from typing import Dict, Any
from pathlib import Path
from .cpp_loader import cpp_loader

logger = logging.getLogger(__name__)

# Указываем путь к библиотеке
lib_dir = Path(__file__).parent / "Release"
dll_path = lib_dir / "comet_calculations.pyd"

if not dll_path.exists():
    raise ImportError(f"Library not found at: {dll_path}")

# Загружаем библиотеку
if not cpp_loader.load_library(str(dll_path)):
    raise ImportError("Failed to load comet_calculations library")

def calculate(file_data: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Расчет температуры сублимации и состава кометы"""
    try:
        required_params = ["H", "Pb", "P", "mu"]
        missing = [p for p in required_params if p not in parameters]
        if missing:
            raise ValueError(f"Missing required parameters: {missing}")

        # Получаем функцию из C++ библиотеки
        calculate_temp = cpp_loader.get_function(
            "calculate_temperature",
            [ctypes.c_double]*4,
            ctypes.c_double
        )
        
        # Вычисляем температуру
        temp = calculate_temp(
            parameters["H"],
            parameters["Pb"],
            parameters["P"],
            parameters["mu"]
        )
        
        # Определяем состав
        estimate_comp = cpp_loader.get_function(
            "estimate_composition",
            [ctypes.c_double],
            ctypes.c_char_p
        )
        composition = estimate_comp(temp).decode('utf-8')
        
        return {
            "value": temp,
            "units": "K",
            "composition": composition
        }
    except Exception as e:
        logger.error(f"Sublimation calculation failed: {str(e)}")
        raise