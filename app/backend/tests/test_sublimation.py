import pytest
from app.backend.app.core.calculations.sublimation import calculate

def test_sublimation_calculation():
    """Тест расчета сублимации с корректными параметрами"""
    params = {
        "H": 5000.0,
        "Pb": 1.013e5,
        "P": 1.0,
        "mu": 18.0
    }
    result = calculate(None, params)
    
    assert isinstance(result["value"], float)
    assert result["units"] == "K"
    assert isinstance(result["composition"], str)
    assert 100 < result["value"] < 300

def test_sublimation_missing_params():
    """Тест с отсутствующими параметрами"""
    params = {
        "H": 5000.0,
        "Pb": 1.013e5
    }
    with pytest.raises(ValueError):
        calculate(None, params)

def test_sublimation_invalid_params():
    """Тест с недопустимыми параметрами"""
    params = {
        "H": -5000.0,  # Отрицательное значение
        "Pb": 1.013e5,
        "P": 1.0,
        "mu": 18.0
    }
    with pytest.raises(Exception):
        calculate(None, params)