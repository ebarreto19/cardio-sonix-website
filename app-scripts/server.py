"""Run script for streamlit application"""

import os
from app import ENTRY_POINT


def main():
    os.system(f"streamlit run {ENTRY_POINT}")


if __name__ == "__main__":
    main()
