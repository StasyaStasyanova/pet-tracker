import flet as ft

class AppState:
    def __init__(self):
        self.tabs: ft.Tabs = None
        self.pet_detail_overlay: ft.Container = None
        self.note_creation_overlay: ft.Container = None
    
    def switch_tab(self, index: int, page: ft.Page = None):
        self.tabs.selected_index = index
        self.tabs.update()
        if page:
            page.update()

app_state = AppState()