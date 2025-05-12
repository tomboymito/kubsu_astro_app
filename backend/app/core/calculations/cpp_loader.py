import ctypes
import platform
from pathlib import Path
import logging


logger = logging.getLogger(__name__)


class CppLoader:
    def __init__(self):
        self._lib = None

    def load_library(self, lib_name):
        try:
            # Определяем расширение файла в зависимости от ОС
            if platform.system() == "Windows":
                lib_ext = ".pyd"
            elif platform.system() == "Linux":
                lib_ext = ".so"
            else:
                # macOS обычно использует .so для Python расширений
                lib_ext = ".so"

            # На macOS и Linux убираем префикс "lib" для Python расширений
            lib_file_name = f"{lib_name}{lib_ext}"

            lib_path = Path(__file__).parent / lib_file_name

            if not lib_path.exists():
                raise FileNotFoundError(f"Library {lib_path} not found")

            self._lib = ctypes.CDLL(str(lib_path))
            logger.info(f"Successfully loaded C++ library: {lib_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load C++ library: {str(e)}")
            self._lib = None
            return False

    def get_function(self, func_name, argtypes, restype):
        if not self._lib:
            raise RuntimeError("Library not loaded")

        func = getattr(self._lib, func_name, None)
        if not func:
            raise AttributeError(f"Function {func_name} not found in library")

        func.argtypes = argtypes
        func.restype = restype
        return func


# Инициализация загрузчика
cpp_loader = CppLoader()
