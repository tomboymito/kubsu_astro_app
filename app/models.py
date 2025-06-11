import math
import numpy as np
from astropy.io import fits

class SublimationModel:
    def __init__(self):
        self.elements_db = [
            # Летучие льды (основные компоненты комет)
            {
                'name': 'H₂O (водяной лёд)',
                'H': 2.83e10,
                'mu': 18,
                'P0': 1e15,
                'P_vap': lambda T: 611 * math.exp(5425*(1/273 - 1/T)),
                'comment': 'Основной компонент кометных ядер. Сублимирует при ~150-200 K'
            },
            {
                'name': 'CO₂ (сухой лёд)',
                'H': 2.3e10,
                'mu': 44,
                'P0': 5.1e6,
                'P_vap': lambda T: 5.1e6 * math.exp(3188*(1/194 - 1/T)),
                'comment': 'Второй по распространённости лёд в кометах'
            },
            {
                'name': 'CO (угарный газ)',
                'H': 1.3e10,
                'mu': 28,
                'P0': 1.15e5,
                'P_vap': lambda T: 1.15e5 * math.exp(764*(1/68 - 1/T)),
                'comment': 'Сублимирует при очень низких температурах'
            },
            {
                'name': 'CH₄ (метан)',
                'H': 1.9e10,
                'mu': 16,
                'P0': 1.3e5,
                'P_vap': lambda T: 1.3e5 * math.exp(1680*(1/91 - 1/T)),
                'comment': 'Обнаружен в кометах 67P и Хартли 2'
            },

            # Другие органические соединения
            {
                'name': 'C₂H₆ (этан)',
                'H': 2.1e10,
                'mu': 30,
                'P0': 2.45e5,
                'P_vap': lambda T: 2.45e5 * math.exp(1980*(1/90 - 1/T)),
                'comment': 'Обнаружен в комете Хейла-Боппа'
            },
            {
                'name': 'CH₃OH (метанол)',
                'H': 3.6e10,
                'mu': 32,
                'P0': 1.23e5,
                'P_vap': lambda T: 1.23e5 * math.exp(4630*(1/175 - 1/T)),
                'comment': 'Важный органический компонент'
            },
            {
                'name': 'H₂CO (формальдегид)',
                'H': 2.8e10,
                'mu': 30,
                'P0': 4.57e5,
                'P_vap': lambda T: 4.57e5 * math.exp(3200*(1/134 - 1/T)),
                'comment': 'Обнаружен в коме комет'
            },

            # Азотистые соединения
            {
                'name': 'NH₃ (аммиак)',
                'H': 2.5e10,
                'mu': 17,
                'P0': 1e5,
                'P_vap': lambda T: 1e5 * math.exp(2000*(1/100 - 1/T)),
                'comment': 'Источник атомарного азота'
            },
            {
                'name': 'HCN (цианистый водород)',
                'H': 3.1e10,
                'mu': 27,
                'P0': 3.47e5,
                'P_vap': lambda T: 3.47e5 * math.exp(3400*(1/150 - 1/T)),
                'comment': 'Важен для пребиотической химии'
            },

            # Сера и её соединения
            {
                'name': 'H₂S (сероводород)',
                'H': 2.7e10,
                'mu': 34,
                'P0': 1.23e6,
                'P_vap': lambda T: 1.23e6 * math.exp(2800*(1/120 - 1/T)),
                'comment': 'Основной источник серы в кометах'
            },
            {
                'name': 'SO₂ (диоксид серы)',
                'H': 3.4e10,
                'mu': 64,
                'P0': 3.82e5,
                'P_vap': lambda T: 3.82e5 * math.exp(4300*(1/180 - 1/T)),
                'comment': 'Обнаружен в комете Хейла-Боппа'
            },

            # Редкие компоненты
            {
                'name': 'N₂ (азот)',
                'H': 1.2e10,
                'mu': 28,
                'P0': 3.5e4,
                'P_vap': lambda T: 3.5e4 * math.exp(500*(1/63 - 1/T)),
                'comment': 'Трудно обнаружить, но важен для эволюции комет'
            },
            {
                'name': 'O₂ (кислород)',
                'H': 1.6e10,
                'mu': 32,
                'P0': 2.5e4,
                'P_vap': lambda T: 2.5e4 * math.exp(600*(1/54 - 1/T)),
                'comment': 'Неожиданно обнаружен в комете 67P'
            }
        ]
        self.data = {}

    def calculate_sublimation(self, input_params):
        try:
            r_sun = float(input_params['r0'])
            r_earth_input = input_params['r_earth'].strip()

            if 'R' in r_earth_input:
                r_earth = float(r_earth_input.replace('R⊕', '').replace('R', '')) * 6371
            else:
                r_earth = float(r_earth_input)

            R_earth = 6371
            sublimating = []
            result_lines = [
                f"Расчётные параметры:",
                f"- Расстояние от Солнца (r☉): {r_sun:.2f} а.е.",
                f"- Расстояние от Земли (r⊕): {r_earth:.2f} км ({r_earth / R_earth:.2f} R⊕)"
            ]

            P_atm = 101325

            for element in self.elements_db:
                H = element.get('H')
                mu = element.get('mu')
                P0 = element.get('P0')

                if not all([H, mu, P0]):
                    continue

                xi = 1 + 0.02 * math.log(P0 / (6.7e14))
                T_sub = 1.3e3 * (1 / xi) * (H / 3.2e10) * (mu / 170) * (r_sun / 1) ** -0.5 * \
                    (1 + 0.1 / (1 + (r_earth / R_earth) ** 2))

                T_input = input_params['T'].strip()
                if T_input:
                    try:
                        T_total = float(T_input)
                    except ValueError:
                        return {"error": "Некорректное значение температуры T"}
                else:
                    if r_earth > 10 * R_earth:
                        T_total = 278 / math.sqrt(r_sun)
                    else:
                        T_sun = 278 / math.sqrt(r_sun)
                        T_earth = 288 * (R_earth / r_earth) ** 0.5 * (1 + 0.3)
                        T_total = (T_sun**4 + T_earth**4)**0.25

                if T_total >= T_sub:
                    if r_earth <= 1.1 * R_earth:
                        P_vap = element['P_vap'](T_total)
                        if P_vap > P_atm:
                            sublimating.append(element['name'])
                    else:
                        sublimating.append(element['name'])

            result_lines.append(f"- Суммарная температура (T_total): {T_total:.2f} K")
            result_lines.append("\nСублимирующие элементы:")
            result_lines.append(", ".join(sublimating) if sublimating else "Нет")

            return {"result": "\n".join(result_lines)}

        except ValueError:
            return {"error": "Проверьте введённые данные!"}
        except Exception as e:
            return {"error": f"Ошибка расчёта: {str(e)}"}

    def load_txt_data(self, file_path):
        key_map_txt = {
            'T': 'T',
            'R0': 'r0',
            'REARTH': 'r_earth',
            'AFRHO0': 'Afρ0',
            'K': 'k',
            'H': 'H',
            'N': 'n',
            'DELTA': 'delta',
            'MK': 'm_k',
            'R': 'r',
            'PV': 'pv',
            'ANGSIZE': 'angular_size'
        }
        with open(file_path, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=')
                    original_key = key.strip()
                    mapped_key = key_map_txt.get(original_key, original_key)
                    self.data[mapped_key] = float(value.strip())

    def load_fits_data(self, file_path):
        key_map_fits = {
            'T': 'T',
            'R0': 'r0',
            'REARTH': 'r_earth',
            'AFRHO0': 'Afρ0',
            'K': 'k',
            'H': 'H',
            'N': 'n',
            'DELTA': 'delta',
            'MK': 'm_k',
            'R': 'r',
            'PV': 'pv',
            'ANGSIZE': 'angular_size'
        }

        with fits.open(file_path) as hdul:
            for hdu in hdul:
                if hasattr(hdu, 'header'):
                    for key, value in hdu.header.items():
                        if isinstance(value, (int, float)):
                            std_key = key_map_fits.get(key, key)
                            self.data[std_key] = value

class GraphModel:
    def __init__(self):
        self.data = {}

    def plot_graph(self, params, graph_type):
        try:
            Afρ0 = float(params['Afρ0'])
            r0 = float(params['r0'])
            k = float(params['k'])
            H = float(params['H'])
            n = float(params['n'])
            delta = float(params['delta'])

            if graph_type == "Afρ от расстояния":
                r = np.linspace(0.1, 5, 100)
                Afρ = Afρ0 * (r / r0) ** (-k)
                return {"x": r, "y": Afρ, "xlabel": "Расстояние от Солнца (а.е.)",
                        "ylabel": "Afρ", "title": "Зависимость Afρ от расстояния",
                        "invert_y": False, "points": False}
            
            elif graph_type == "Звездной величины от расстояния":
                r = np.linspace(0.1, 5, 100)
                m = H + 5 * np.log10(delta) + 2.5 * n * np.log10(r)
                return {"x": r, "y": m, "xlabel": "Расстояние от Солнца (а.е.)",
                        "ylabel": "Звездная величина (m)", "title": "Зависимость звездной величины от расстояния",
                        "invert_y": True, "points": False}
                
            elif graph_type == "Afρ от даты":
                t = np.linspace(-50, 50, 100)
                t0 = 0
                tau = 10
                Afρ = Afρ0 * np.exp(-(t - t0) ** 2 / (2 * tau ** 2))
                return {"x": t, "y": Afρ, "xlabel": "Время (дни)",
                        "ylabel": "Afρ", "title": "Зависимость Afρ от времени",
                        "invert_y": False, "points": False}
                
            elif graph_type == "Звездной величины от даты":
                t = np.linspace(-50, 50, 100)
                r = np.clip(r0 + 0.01 * t, 1e-3, None)
                m = H + 5 * np.log10(delta) + 2.5 * n * np.log10(r)
                return {"x": t, "y": m, "xlabel": "Время (дни)",
                        "ylabel": "Звездная величина (m)", "title": "Зависимость звездной величины от времени",
                        "invert_y": True, "points": False}

        except ValueError as e:
            return {"error": "Пожалуйста, проверьте введенные данные"}
        except Exception as e:
            return {"error": f"Произошла ошибка при построении графика: {str(e)}"}

class MassModel:
    def __init__(self):
        self.data = {}

    def calculate_mass(self, params):
        try:
            m_k = float(params['m_k'])
            delta = float(params['delta'])
            r = float(params['r'])
            
            m_nk = -13.78
            f_c2 = 0.031
            
            numerator = 10**(-0.4 * (m_k - m_nk)) * delta**2 * r**2
            denominator = 1.37 * 10**(-38) * f_c2
            N = numerator / denominator
            
            N_kg = N
            N_tons = N / 1000
            N_megatons = N / 1e9
            
            return {
                "result": f"Полная масса, выделяемая кометой (N):\n"
                          f"{N_kg:.2e} кг\n"
                          f"{N_tons:.2e} тонн\n"
                          f"{N_megatons:.2e} мегатонн"
            }
            
        except ValueError:
            return {"error": "Пожалуйста, проверьте введенные данные"}
        except Exception as e:
            return {"error": f"Произошла ошибка при расчетах: {str(e)}"}

class SizeModel:
    def __init__(self):
        self.data = {}

    def calculate_size(self, params):
        try:
            H = float(params['H'])
            pv = float(params['pv'])
            angular_size = float(params['angular_size']) if params['angular_size'] else 0
            
            if not 0 < pv <= 1:
                raise ValueError("Альбедо должно быть в диапазоне (0, 1]")
            if angular_size < 0:
                raise ValueError("Угловой размер не может быть отрицательным")
            
            D = 1329 / math.sqrt(pv) * 10**(-0.2 * H)
            
            linear_size_info = ""
            if angular_size > 0:
                distance_au = float(params.get('distance', 1.0))
                distance_km = distance_au * 149.6e6
                linear_size_km = distance_km * math.tan(math.radians(angular_size / 3600))
                linear_size_info = (f"\nЛинейный размер при {angular_size}\": {linear_size_km:.2f} км "
                                f"(на расстоянии {distance_au:.2f} а.е.)")
            
            return {
                "result": f"Диаметр ядра кометы: {D:.2f} км\n"
                          f"Геометрическое альбедо (p_v): {pv:.3f}\n"
                          f"Абсолютная звёздная величина (H): {H:.2f}"
                          + linear_size_info
            }
            
        except ValueError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Произошла ошибка: {str(e)}"}