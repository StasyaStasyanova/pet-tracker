import flet as ft

GREETING_TEXTS = {
    True: "Привет! Как себя чувствует {}?",
    False: "Привет! У вас ещё нет добавленных питомцев("
}

class MainTab(ft.Tab):
    def __init__(self):
        super().__init__()
        self.label = "Главная"

class MainContainer(ft.Container):
    def __init__(self):
        super().__init__()
        self.content=ft.Text(value=GREETING_TEXTS[False])
        self.alignment=ft.Alignment.CENTER