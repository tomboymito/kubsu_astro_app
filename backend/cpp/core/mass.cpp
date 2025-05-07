#include "../include/mass.h"
#include <stdexcept>
#include <cmath>

namespace comet {

double MassCalculator::calculate_mass(double m_k, double m_sun, double delta, double r, double f_C2) {
    if (m_k <= 0 || m_sun <= 0 || delta <= 0 || r <= 0 || f_C2 <= 0) {
        throw std::invalid_argument("Parameters must be positive");
    }
    // Формула: N = 10^(-0.4(m_k - m_lk)) * Δ^2 * r^2 / (1.37e-38 * f(C2))
    // Здесь m_lk не передается, предполагается, что m_lk = 0 для упрощения
    double numerator = std::pow(10, -0.4 * (m_k)) * delta * delta * r * r;
    double denominator = 1.37e-38 * f_C2;
    if (denominator == 0) {
        throw std::runtime_error("Denominator in mass calculation is zero");
    }
    return numerator / denominator;
}

} // namespace comet
