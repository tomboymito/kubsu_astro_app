import pytest
from app.core.calculations.sublimation import calculate_temperature


def test_sublimation_temperature_calculation():
    # Тест с нормальными параметрами
    H = 5000
    Pb = 1.013e5
    P = 1.0
    mu = 18.0

    result = calculate_temperature(H, Pb, P, mu)
    assert isinstance(result, float)
    assert 100 < result < 300  # Ожидаемый диапазон температур

    # Тест с нулевым знаменателем
    with pytest.raises(ValueError):
        calculate_temperature(H, Pb, Pb, mu)  # Pb и P равны, знаменатель 0
