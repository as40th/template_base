# data/__init__.py (загрузчик данных)

"""
data/ — Данные (ресурсы)

Назначение: Статические данные, которые используются приложением: датасеты, эмбеддинги, справочники.
Особенности:
- Могут быть большими файлами
- Не являются кодом
- Не должны попадать в Git (кроме примеров)
"""
from pathlib import Path
import json
import numpy as np

DATA_DIR = Path(__file__).parent

def load_countries() -> dict:
    """Загрузка списка стран из JSON"""
    path = DATA_DIR / "datasets" / "countries.json"
    with open(path) as f:
        return json.load(f)

def load_embedding_matrix() -> np.ndarray:
    """Загрузка матрицы эмбеддингов"""
    path = DATA_DIR / "embeddings" / "sample_embeddings.npy"
    return np.load(path)