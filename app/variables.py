"""Global variables"""

__all__ = [
    "CONFIG_DIR",
    "ENTRY_POINT",
    "ASSETS_DIR",
    "THEME_DIR",
    "GIF_DIR",
    "IMAGES_DIR",
    "VIDEOS_DIR",
    "END_POINT_PREDICT"
]

from pathlib import Path


# --- PATH SETTINGS ---
APP_DIR: Path = Path(__file__).parent if "__file__" in locals() else Path.cwd()
ROOT_DIR: Path = APP_DIR.parent
CONFIG_DIR: Path = ROOT_DIR / ".streamlit"
ENTRY_POINT = APP_DIR / "⭐️_Home.py"
ASSETS_DIR: Path = APP_DIR / "assets"
THEME_DIR: Path = APP_DIR / "theme"
GIF_DIR: Path = ASSETS_DIR / "gif"
IMAGES_DIR: Path = ASSETS_DIR / "images"
VIDEOS_DIR: Path = ASSETS_DIR / "videos"


# --- Cardio Sonix API ---
API_HOST: str = "http://127.0.0.1:8000"
END_POINT_PREDICT: str = API_HOST + "/predict"
