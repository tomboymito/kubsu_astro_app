import ctypes
import platform
from pathlib import Path
import logging
import os

logger = logging.getLogger(__name__)

class CppLoader:
    def __init__(self):
        self._lib = None
        self._lib_ext = ".pyd" if platform.system() == "Windows" else ".so"

    def load_library(self, lib_name: str) -> bool:
        """Загружает C++ библиотеку с проверкой нескольких возможных путей"""
        possible_paths = [
            Path(__file__).parent / f"{lib_name}{self._lib_ext}",
            Path(__file__).parent.parent / f"{lib_name}{self._lib_ext}",
            Path(os.getcwd()) / f"{lib_name}{self._lib_ext}"
        ]

        for lib_path in possible_paths:
            try:
                if lib_path.exists():
                    self._lib = ctypes.CDLL(str(lib_path))
                    logger.info(f"Successfully loaded C++ library from {lib_path}")
                    return True
            except Exception as e:
                logger.warning(f"Failed to load from {lib_path}: {str(e)}")

        logger.error(f"Could not find library {lib_name} in any of: {possible_paths}")
        return False

    def get_function(self, func_name: str, argtypes: list, restype):
        """Получает функцию из загруженной библиотеки с проверками"""
        if not self._lib:
            raise RuntimeError("Library not loaded")

        func = getattr(self._lib, func_name, None)
        if not func:
            raise AttributeError(f"Function {func_name} not found in library")

        try:
            func.argtypes = argtypes
            func.restype = restype
            return func
        except Exception as e:
            logger.error(f"Failed to configure function {func_name}: {str(e)}")
            raise

# Инициализация загрузчика
cpp_loader = CppLoader()