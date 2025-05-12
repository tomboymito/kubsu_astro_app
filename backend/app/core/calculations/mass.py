import numpy as np
from typing import Dict, Any
import logging


logger = logging.getLogger(__name__)


def calculate_mass(
    m_k: float,
    m_sun: float,
    delta: float,
    r: float,
    f_C2: float = 1.0,
) -> float:
    # Исправлено: разбивка длинной строки функции для соответствия Flake8 E501
    """
    Расчет массы кометы по формуле:
    N = 10^(-0.4*(m_k - m_sun)) * delta^2 * r^2 / \
        (1.37e-38 * f(C2))
    """
    try:
        term1 = 10 ** (-0.4 * (m_k - m_sun))
        term2 = delta ** 2 * r ** 2
        denominator = 1.37e-38 * f_C2

        if denominator == 0:
            raise ValueError("Denominator in mass formula equals zero")

        mass = term1 * term2 / denominator
        return mass
    except Exception as e:
        logger.error(f"Error in mass calculation: {str(e)}")
        raise


def calculate(file_data: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Основная функция расчета массы кометы"""
    try:
        # Проверка
        # наличия данных
        if file_data is None or "magnitude" not in file_data:
            raise ValueError("Missing magnitude data in input file")

        # Параметры по умолчанию
        default_params = {
            # Звездная величина Солнца
            "m_sun": -26.74,
            # Геоцентрическое расстояние [а.е.]
            "delta": 1.0,
            # Гелиоцентрическое расстояние [а.е.]
            "r": 1.0,
            # Поправочный коэффициент для C2
            "f_C2": 1.0,
        }

        # Обновление параметров пользовательскими значениями
        params = {**default_params, **parameters}

        # Используем среднюю звездную величину из данных
        m_k = np.mean(file_data["magnitude"])

        # Расчет массы
        mass = calculate_mass(m_k, params["m_sun"], params["delta"], params["r"], params["f_C2"])

        return {
            "value": mass,
            "units": "kg",
            "method": "photometric",
        }
    except Exception as e:
        logger.error(f"Mass calculation failed: {str(e)}")
        raise
