from typing import Dict, Any
import logging
import ctypes
from app.core.calculations.cpp_loader import cpp_loader


logger = logging.getLogger(__name__)


# Загрузка C++ библиотеки при импорте модуля
cpp_loader.load_library("libcomet_calculations")


try:
    # Получаем функции из C++ библиотеки
    calculate_temp = cpp_loader.get_function(
        "calculate_sublimation_temperature",
        [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double],
        ctypes.c_double
    )

    estimate_comp = cpp_loader.get_function(
        "estimate_comet_composition",
        [ctypes.c_double],
        ctypes.c_char_p
    )
except Exception as e:
    logger.error(f"Failed to load C++ functions: {str(e)}")
    raise


def calculate(file_data: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Python-обертка для C++ расчета сублимации"""
    try:
        # Параметры по умолчанию
        default_params = {
            "H": 5000.0,
            "Pb": 1.013e5,
            "P": 1.0,
            "mu": 18.0
        }

        # Обновление параметров
        params = {**default_params, **parameters}

        # Вызов C++ функции
        Tsub = calculate_temp(
            params["H"], params["Pb"], params["P"], params["mu"]
        )

        # Получение состава
        composition = estimate_comp(Tsub).decode('utf-8')

        return {
            "value": Tsub,
            "units": "K",
            "composition": composition
        }
    except Exception as e:
        logger.error(f"Sublimation calculation failed: {str(e)}")
        raise
