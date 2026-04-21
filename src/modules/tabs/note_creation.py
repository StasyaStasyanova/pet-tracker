import flet as ft

from modules.models.note import Note
from modules.models.pet import Pet

class NoteCreationOverlay(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._detail_content = ft.Column(
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color=ft.Colors.GREY_100,
                            on_click=self._close,
                        ),
                    ],
                ),
                self._detail_content,
            ],
            spacing=12,
        )
        self.bgcolor = ft.Colors.GREY_800
        self.padding = 20
        self.expand = True
        self.visible = False

    def show_note(self, pet: Pet = None):
        dd_disabled = False
        pets = Pet.select()
        pets_dropdown_options = []
        if pet:
            dd_disabled = True
            pets_dropdown_options.append(ft.dropdown.Option(key=pet.id, text=pet.name))
        else:
            for pet in pets:
                pets_dropdown_options.append(ft.dropdown.Option(key=pet.id, text=pet.name))
        self.current_pet = pets_dropdown_options[0].key if pets_dropdown_options else None
        self.note_content = ft.TextField(label="Заметка", multiline=True, on_change=self._page.update)
        self._detail_content.controls = [
            ft.Text("Тут можно будет создать заметку", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_100),
            self.note_content,
            ft.Dropdown(value=self.current_pet, options=pets_dropdown_options, label="Выберите питомца", disabled=dd_disabled),
            ft.Button(content=ft.Text("Создать"), color=ft.Colors.PRIMARY, on_click=self.add_note),
        ]
        self.visible = True
        self._page.overlay.append(self)
        self._page.update()

    def add_note(self, e):
        pet = Pet.get_by_id(self.current_pet)
        Note.create(content = self.note_content.value, pet = pet)

    def _close(self):
        self.visible = False
        self._page.overlay.remove(self)
        self._page.update()