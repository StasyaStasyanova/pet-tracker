import flet as ft
from peewee import *

from modules.models.note import Note
from utils import WELLBEING_COLORS
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
    def __init__(self, task: asyncio.Task = None):
        super().__init__()
        self._pets = list(Pet.select())
        self._current_index = 0
        self._running = False
        self._displays: list[PetDisplayCompact] = []
        self.cycle_task = task

        if not self._pets:
            main_content = ft.Column(
                controls=[
                    ft.Text(
                    GREETING_TEXTS[False],
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.ON_SURFACE,
                    ),
                ],
                spacing=16,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
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
                color=ft.Colors.ON_SURFACE,
                opacity=1.0,
                animate_opacity=ft.Animation(600, ft.AnimationCurve.EASE_IN_OUT),
            )

            greeting = ft.Row(
                controls=[
                    ft.Text(
                        "Привет! Как себя чувствует ",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.ON_SURFACE,
                    ),
                    self._name_text,
                ],
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                wrap=True,
            )

            pet_stack = ft.Stack(
                controls=self._displays,
                width=300,
                height=372,
            )

            main_content = ft.Column(
                controls=[greeting, pet_stack],
                spacing=16,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
            )

        self.content = main_content
        self.alignment = ft.Alignment.CENTER
        self.padding = 20
        
        recent_notes = Note.select().order_by(Note.created_at.desc()).limit(3)
            
        activity_title = ft.Row(
            controls=[
                ft.Icon(ft.Icons.PETS, size=20, color=ft.Colors.PRIMARY),
                ft.Text(
                    "Последняя активность",
                    size=18,
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.ON_SURFACE,
                ),
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        if not recent_notes.exists():
            notes_section = ft.Container(
                content=ft.Column(
                    controls=[
                        activity_title,
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Icon(ft.Icons.NOTE_ADD, size=40, color=ft.Colors.ON_SURFACE_VARIANT),
                                    ft.Text(
                                        "Нет недавних записей",
                                        size=14,
                                        color=ft.Colors.ON_SURFACE_VARIANT,
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=8,
                            ),
                            padding=ft.Padding.all(20),
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                            border_radius=12,
                            width=300,
                        ),
                    ],
                    spacing=12,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                margin=ft.Margin.only(top=20),
            )
        else:
            note_displays = []
            for note in recent_notes:
                note_displays.append(self._create_mini_note_display(note))
            
            notes_section = ft.Container(
                content=ft.Column(
                    controls=[
                        activity_title,
                        ft.Row(
                            controls=note_displays,
                            spacing=8,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    spacing=12,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                margin=ft.Margin.only(top=20),
            )

        self.content.controls.append(notes_section)

        self.alignment = ft.Alignment.CENTER
        self.padding = 20
        self.expand = True

    def _create_mini_note_display(self, note: Note):
        wellbeing_dots = ft.Row(
            controls=[
                ft.Container(
                    width=6,
                    height=6,
                    border_radius=3,
                    bgcolor=WELLBEING_COLORS.get(note.overall_wellbeing, ft.Colors.GREEN_400)
                    if i < note.overall_wellbeing
                    else ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                )
                for i in range(5)
            ],
            spacing=2,
        )
        
        date_str = note.created_at.strftime('%d %b, %H:%M')

        stats = []
        if note.energy:
            stats.append(f"🗲 {note.energy}")
        if note.appetite:
            stats.append(f"🍽️ {note.appetite}")
        if note.mood:
            stats.append(f"☻ {note.mood}")
        if note.activity:
            stats.append(f"➹ {note.activity}")
        
        stats_text1 = "  ✧  ".join(stats[:2]) if stats else "Нет данных"
        stats_text2 = "  ✧  ".join(stats[2:]) if stats else ""
        stats_text = f"{stats_text1}\n{stats_text2}"
        
        note_text = f"✎ {note.content}" or ""
        if len(note_text) > 60:
            note_text = note_text[:57] + "..."
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                f"{note.pet.name}",
                                size=16,
                                weight=ft.FontWeight.W_600,
                                color=ft.Colors.ON_SURFACE,
                                expand=True,
                            ),
                            ft.Text(
                                date_str,
                                size=11,
                                color=ft.Colors.ON_SURFACE_VARIANT,
                            ),
                        ],
                        spacing=6,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            wellbeing_dots,
                            ft.Text(
                                f"{note.overall_wellbeing}/5",
                                size=12,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.ON_SURFACE,
                            ),
                        ],
                        spacing=6,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Text(
                        stats_text,
                        size=16,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                    ft.Text(
                        value="______________________",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),    
                    ),
                    ft.Text(
                        note_text,
                        size=12,
                        color=ft.Colors.with_opacity(0.7, ft.Colors.WHITE),
                        visible=bool(note_text),
                    ),
                ],
                spacing=6,
            ),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            border_radius=10,
            padding=ft.Padding.all(12),
            width=500,
            height=200,
            on_click=self.note_clicked,
        )
                
    def note_clicked(self):
        from modules.appState import app_state
        from utils import TABS
        app_state.switch_tab(TABS.NOTES.value)
                
    def did_mount(self):
        if len(self._displays) > 1:
            self._running = True
            if self.cycle_task:
                self.cycle_task.cancel()
            self.cycle_task = asyncio.ensure_future(self._cycle_pets())

    def rebuild(self):
        self.__init__(task=self.cycle_task)
        self.did_mount()
        self.page.update()

    def will_unmount(self):
        self._running = False
        if self.cycle_task:
            self.cycle_task.cancel()

    async def _cycle_pets(self):
        while self._running:
            await asyncio.sleep(3)

            next_index = (self._current_index + 1) % len(self._displays)

            self._displays[self._current_index].opacity = 0
            self._displays[self._current_index].update()
            self._name_text.opacity = 0
            self._name_text.update()

            await asyncio.sleep(0.65)

            if not self._running:
                break

            self._current_index = next_index
            self._name_text.value = self._pets[self._current_index].name + "?"

            self._displays[self._current_index].opacity = 1
            self._displays[self._current_index].update()
            self._name_text.opacity = 1
            self._name_text.update()
    
    def _on_display_clicked(self):
        _on_pet_display_clicked(self._displays[self._current_index].pet)