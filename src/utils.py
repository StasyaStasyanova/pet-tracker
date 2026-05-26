from pathlib import Path
from enum import Enum
import os
ROOT_DIR = Path(__file__).parent
DATA_DIR = os.path.join(ROOT_DIR, 'data')

class TABS(Enum):
    MAIN = 0
    PETS = 1
    NOTES = 2
    CALENDAR = 3

WELLBEING_IMAGES = {
    1: os.path.join(ROOT_DIR, 'assets/wellbeing/awful.png'),
    2: os.path.join(ROOT_DIR, 'assets/wellbeing/bad.png'),
    3: os.path.join(ROOT_DIR, 'assets/wellbeing/neutral.png'),
    4: os.path.join(ROOT_DIR, 'assets/wellbeing/good.png'),
    5: os.path.join(ROOT_DIR, 'assets/wellbeing/awesome.png'),
}