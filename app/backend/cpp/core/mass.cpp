#include "../include/mass.h"
#include <stdexcept>
#include <cmath>

namespace comet {

double MassCalculator::calculate_mass(double m_k, double m_sun, double delta, double r, double f_C2) {
    // Проверка параметров
    if (delta <= 0 || r <= 0 || f_C2 <= 0) {
        throw std::invalid_argument("Delta, r and f_C2 must be positive");
    }

    // Расчет числителя: 10^(-0.4*(m_k - m_sun)) * delta^2 * r^2
    double term1 = std::pow(10, -0.4 * (m_k - m_sun));
    double term2 = delta * delta * r * r;
    double numerator = term1 * term2;

    // Расчет знаменателя: 1.37e-38 * f_C2
    double denominator = 1.37e-38 * f_C2;
    
    if (denominator == 0) {
        throw std::runtime_error("Denominator in mass calculation is zero");
    }

    return numerator / denominator;
}

} // namespace comet