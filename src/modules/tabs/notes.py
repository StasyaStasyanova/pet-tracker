import flet as ft

class NotesTab(ft.Tab):
    def __init__(self):
        super().__init__()
        self.label = "Заметки"

class NotesContainer(ft.Container):
    def __init__(self):
        super().__init__()
        self.content=ft.Text("Заметки")
        self.alignment=ft.Alignment.CENTER