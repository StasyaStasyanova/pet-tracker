import flet as ft

class AppState:
    def __init__(self):
        self.tabs: ft.Tabs = None
    
    def switch_tab(self, index: int, page: ft.Page):
        self.tabs.selected_index = index
        page.update()

app_state = AppState()