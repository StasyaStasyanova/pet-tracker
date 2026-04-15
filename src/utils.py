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