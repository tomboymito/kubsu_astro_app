#include "../include/nucleus.h"
#include <stdexcept>
#include <cmath>

namespace comet {

double NucleusCalculator::calculate_diameter(double A, double p, double H) {
    if (A <= 0 || p <= 0 || H <= 0) {
        throw std::invalid_argument("Parameters must be positive");
    }
    // Формула: D = q * 4A / (π p H)
    // В ТЗ q не определён, предположим q = 1 для упрощения
    const double q = 1.0;
    return q * 4.0 * A / (M_PI * p * H);
}

} // namespace comet
