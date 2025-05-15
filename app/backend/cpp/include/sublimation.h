#ifndef SUBLIMATION_H
#define SUBLIMATION_H

#include <string>

namespace comet {

class SublimationCalculator {
public:
    static double calculate_temperature(double H, double P0, double P, double mu);
    static std::string estimate_composition(double temperature);
};

} // namespace comet

#endif // SUBLIMATION_H
