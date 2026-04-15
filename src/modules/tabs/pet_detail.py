import flet as ft
from datetime import datetime
import os
import shutil
from modules.models.pet import Pet
from .pets import calculate_age, name_year

class PetDetailOverlay(ft.Container):
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
        self.bgcolor = ft.Colors.GREY_800  # matches your dark theme bg
        self.padding = 20
        self.expand = True
        self.visible = False

    def show_pet(self, pet: Pet):
        self._detail_content.controls = [
            ft.Text(pet.name, size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_100),
            ft.Text(str(pet.AnimalType), size=16, color=ft.Colors.GREY_400),
            ft.Text(
                f"{calculate_age(pet.birthday)} {name_year(calculate_age(pet.birthday))}",
                size=14,
                color=ft.Colors.BLUE_200,
            ),
            # add whatever other fields you want here
        ]
        self.visible = True
        self._page.overlay.append(self)
        self._page.update()

    def _close(self, e):
        self.visible = False
        self._page.overlay.remove(self)
        self._page.update()