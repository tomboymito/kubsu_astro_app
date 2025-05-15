import sys
from pathlib import Path

# Добавляем корень проекта в PYTHONPATH
root = Path(__file__).parent
sys.path.insert(0, str(root))