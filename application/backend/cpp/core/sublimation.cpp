#include "../include/sublimation.h"
#include <cmath>
#include <stdexcept>
#include <string>
#include <sstream>


namespace comet {


double SublimationCalculator::calculate_temperature(double H, double P0, double P, double mu) {
    if (P0 <= 0 || P <= 0 || mu <= 0) {
        throw std::invalid_argument("Pressure and mu must be positive");
    }
    double denominator = std::log(P0) - std::log(P) + std::log(mu);
    if (denominator == 0) {
        throw std::runtime_error("Denominator in temperature calculation is zero");
    }
    return H / denominator;
}


std::string SublimationCalculator::estimate_composition(double temperature) {
    if (temperature < 50) {
        return "CO, CO2, N2 (Volatile ices)";
    } else if (temperature < 150) {
        return "H2O (Water ice)";
    } else {
        return "Silicates, metals (Refractory materials)";
    }
}


} // namespace comet
