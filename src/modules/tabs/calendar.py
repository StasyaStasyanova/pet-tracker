import flet as ft

class CalendarTab(ft.Tab):
    def __init__(self):
        super().__init__()
        self.label = "Календарь"

class CalendarContainer(ft.Container):
    def __init__(self):
        super().__init__()
        self.content=ft.Text("Календарь")
        self.alignment=ft.Alignment.CENTER