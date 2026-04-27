import flet as ft
import os
from modules.models.pet import Pet
from .pets import calculate_age, name_year
from modules.appState import app_state
from utils import TABS

class PetDetailOverlay(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self.pet = None
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
                            icon_color=ft.Colors.ON_SURFACE,
                            on_click=self._close,
                        ),
                    ],
                ),
                self._detail_content,
                ft.Button(content=ft.Text("Добавить заметку"), color=ft.Colors.PRIMARY, on_click=self.notes_button_clicked),
            ],
            spacing=12,
        )
        self.bgcolor = ft.Colors.SURFACE
        self.padding = 20
        self.expand = True
        self.visible = False
    
    def notes_button_clicked(self):
        from modules.appState import app_state
        app_state.note_creation_overlay.show_note(self.pet)
        self._close()

    def show_pet(self, pet: Pet):
        self.pet = pet
        has_image = pet.image and os.path.exists(pet.image)
        
        self._detail_content.controls = [
            ft.Image(src=pet.image, width=64, height=64, fit=ft.BoxFit.COVER,
            ) if has_image else ft.Icon(ft.Icons.PETS, size=32, color=ft.Colors.PRIMARY),
            ft.Text(pet.name, size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE),
            ft.Text(str(pet.AnimalType), size=16, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Text(str(pet.birthday)[0:10], size=16, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Text(
                f"{calculate_age(pet.birthday)} {name_year(calculate_age(pet.birthday))}",
                size=14,
                color=ft.Colors.PRIMARY,
            ),
        ]
        self.visible = True
        self._page.overlay.append(self)
        self._page.update()
        
    def _close(self):
        self.visible = False
        self._page.overlay.remove(self)
        self._page.update()