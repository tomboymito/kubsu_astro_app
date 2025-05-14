from app.core.calculations.sublimation import calculate  # Используйте calculate вместо calculate_temperature

def test_sublimation():
    # Тестовые параметры
    params = {
        "H": 5000.0,
        "Pb": 1.013e5,
        "P": 1.0,
        "mu": 18.0
    }
    result = calculate(None, params)
    assert isinstance(result["value"], float)