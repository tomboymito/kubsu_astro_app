class FakeCppLoader:
    def get_function(self, name, argtypes, restype):
        if name == 'calculate_temperature':
            return lambda H, Pb, P, mu: 42.0  # Заглушка
        raise AttributeError(f"Function {name} not found")

cpp_loader = FakeCppLoader()