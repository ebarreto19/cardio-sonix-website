"""Global variables"""

__all__ = [
    "ROOT_DIR",
    "GIF_DIR",
    "IMAGES_DIR"
]

from pathlib import Path


# --- PATH SETTINGS ---
ROOT_DIR: Path = Path(__file__).parent.parent if "__file__" in locals() else Path.cwd().parent
ASSETS_DIR: Path = ROOT_DIR / "assets"
GIF_DIR: Path = ASSETS_DIR / "gif"
IMAGES_DIR: Path = ASSETS_DIR / "images"
