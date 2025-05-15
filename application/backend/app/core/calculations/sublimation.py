import ctypes
import logging
from pathlib import Path
from typing import Dict, Any  # Добавлен импорт типов
try:
    from .cpp_loader import cpp_loader
except ImportError:
    from .fake_cpp import cpp_loader  # Используем заглушку

logger = logging.getLogger(__name__)

# Путь к библиотеке относительно текущего файла
lib_dir = Path(__file__).parent
dll_path = lib_dir / "comet_calculations.pyd"

if not dll_path.exists():
    raise ImportError(f"Library not found at: {dll_path}. Please build C++ module first.")

# Загружаем библиотеку
if not cpp_loader.load_library(str(dll_path)):
    raise ImportError(f"Failed to load comet_calculations library from {dll_path}")

def calculate(file_data: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Основная функция расчета сублимации"""
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
        
        temp = calculate_temp(
            parameters["H"],
            parameters["Pb"],
            parameters["P"],
            parameters["mu"]
        )
        
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