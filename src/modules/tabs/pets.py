import flet as ft

class PetsTab(ft.Tab):
    def __init__(self):
        super().__init__()
        self.label = "Питомцы"

class PetsContainer(ft.Container):
    def __init__(self):
        super().__init__()
        self.content=ft.Text("Питомцы")
        self.alignment=ft.Alignment.CENTER