#ifndef MASS_H
#define MASS_H

namespace comet {

class MassCalculator {
public:
    static double calculate_mass(double m_k, double m_sun, double delta, double r, double f_C2);
};

} // namespace comet

#endif // MASS_H
