import sys
import os
from pathlib import Path
from .cpp_loader import cpp_loader

# Указываем правильный путь к библиотеке
lib_dir = Path(__file__).parent / "Release"
dll_path = lib_dir / "comet_calculations.pyd"

if not dll_path.exists():
    raise ImportError(f"Library not found at: {dll_path}")

# Загружаем библиотеку
if not cpp_loader.load_library(str(dll_path)):
    raise ImportError("Failed to load comet_calculations library")