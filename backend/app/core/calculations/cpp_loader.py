import ctypes
import platform
from pathlib import Path
import logging
import os

logger = logging.getLogger(__name__)

class CppLoader:
    def __init__(self):
        self._lib = None
        self._lib_ext = {
            "Windows": ".pyd",
            "Linux": ".so",
            "Darwin": ".so"
        }.get(platform.system(), ".so")

    def load_library(self, lib_path: str) -> bool:
        """Загружает библиотеку по полному пути"""
        try:
            lib_path = str(Path(lib_path).with_suffix(self._lib_ext))
            self._lib = ctypes.CDLL(lib_path)
            logger.info(f"Successfully loaded library: {lib_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load library: {str(e)}")
            self._lib = None
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