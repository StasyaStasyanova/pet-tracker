import flet as ft
from peewee import *
from ..models.pet import Pet
from .pets import PetDisplayCompact, _on_pet_display_clicked
import asyncio

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
        self._pets = list(Pet.select())
        self._current_index = 0
        self._running = False
        self._displays: list[PetDisplayCompact] = []

        if not self._pets:
            main_content = ft.Text(
                GREETING_TEXTS[False],
                size=30,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.GREY_100,
            )
        else:
            for i, pet in enumerate(self._pets):
                display = PetDisplayCompact(pet, image_size=(300, 300), width=300, on_click=lambda: self._on_display_clicked())
                display.opacity = 1.0 if i == 0 else 0.0
                display.animate_opacity = ft.Animation(600, ft.AnimationCurve.EASE_IN_OUT)
                self._displays.append(display)

            self._name_text = ft.Text(
                self._pets[0].name + "?",
                weight=ft.FontWeight.BOLD,
                size=24,
                color=ft.Colors.GREY_100,
                opacity=1.0,
                animate_opacity=ft.Animation(600, ft.AnimationCurve.EASE_IN_OUT),
            )

            greeting = ft.Row(
                controls=[
                    ft.Text(
                        "Привет! Как себя чувствует ",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_100,
                    ),
                    self._name_text,
                ],
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                wrap=True,
            )

            pet_stack = ft.Stack(
                controls=self._displays,
                width=300,   # match card width
                height=372,  # 90px avatar + 10px spacing + ~30px name + 32px vertical padding
            )

            main_content = ft.Column(
                controls=[greeting, pet_stack],
                spacing=16,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )

        self.content = main_content
        self.alignment = ft.Alignment.CENTER
        self.padding = 20

    def did_mount(self):
        if len(self._displays) > 1:
            self._running = True
            self.page.run_task(self._cycle_pets)

    def will_unmount(self):
        self._running = False

    async def _cycle_pets(self):
        while self._running:
            await asyncio.sleep(3)

            next_index = (self._current_index + 1) % len(self._displays)

            # Fade out current card + name
            self._displays[self._current_index].opacity = 0
            self._displays[self._current_index].update()
            self._name_text.opacity = 0
            self._name_text.update()

            await asyncio.sleep(0.65)

            if not self._running:
                break

            # Swap content
            self._current_index = next_index
            self._name_text.value = self._pets[self._current_index].name + "?"

            # Fade in next card + name
            self._displays[self._current_index].opacity = 1
            self._displays[self._current_index].update()
            self._name_text.opacity = 1
            self._name_text.update()
    
    def _on_display_clicked(self):
        _on_pet_display_clicked(self._displays[self._current_index].pet)