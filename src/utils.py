from pathlib import Path
from enum import Enum
from os import getenv
ROOT_DIR = Path(getenv("FLET_APP_STORAGE_DATA")) if getenv("FLET_APP_STORAGE_DATA") else Path(__file__).parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

class TABS(Enum):
    MAIN = 0
    PETS = 1
    NOTES = 2
    CALENDAR = 3

WELLBEING_IMAGES = {
    1: 'wellbeing/awful.png',
    2: 'wellbeing/bad.png',
    3: 'wellbeing/neutral.png',
    4: 'wellbeing/good.png',
    5: 'wellbeing/awesome.png'
}

WELLBEING_COLORS = {
    1: '#2E5171',
    2: '#3688B0',
    3: '#25A984',
    4: '#59DE4F',
    5: '#E5FF00'
}