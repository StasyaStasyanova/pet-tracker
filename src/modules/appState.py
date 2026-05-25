import flet as ft

class AppState:
    def __init__(self):
        from modules.tabs.main import MainTab
        from modules.tabs.pets import PetsTab
        from modules.tabs.notes import NotesTab
        from modules.tabs.calendar import CalendarTab
        from modules.tabs.main import MainContainer
        from modules.tabs.pets import PetsContainer
        from modules.tabs.notes import NotesContainer
        from modules.tabs.calendar import CalendarContainer
        self.tabs: ft.Tabs = None
        self.pet_detail_overlay: ft.Container = None
        self.note_creation_overlay: ft.Container = None
        self.mainTab: MainTab = None
        self.petsTab: PetsTab = None
        self.notesTab: NotesTab = None
        self.calendarTab: CalendarTab = None
        self.mainContainer: MainContainer = None
        self.petsContainer: PetsContainer = None
        self.notesContainer: NotesContainer = None
        self.calendarContainer: CalendarContainer = None
    
    def switch_tab(self, index: int, page: ft.Page = None):
        self.tabs.selected_index = index
        self.tabs.update()
        if page:
            page.update()
    
    def update_lists(self):
        self.petsContainer.load_pets()
        self.notesContainer.load_notes()
        self.mainContainer.rebuild()
        self.calendarContainer._build_month()

app_state = AppState()