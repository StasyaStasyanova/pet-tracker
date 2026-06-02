from pathlib import Path
from enum import Enum
from os import getenv
import flet as ft
from datetime import datetime
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

class YearPicker():
    def __init__(self, on_change = None):
        self.current_year = datetime.now().year
        self.years = [str(y) for y in range(self.current_year - 50, self.current_year + 11)]

        self.dropdown = ft.Dropdown(
            value = str(self.current_year),
            options = [ft.DropdownOption(key=y, text=y) for y in reversed(self.years)],
            on_select = on_change,
            menu_height=200,
            border_color=ft.Colors.TRANSPARENT,
            trailing_icon=None
        )
    
    def change_year_option(self, year: int):
        self.dropdown.value = str(year)
        self.dropdown.update()