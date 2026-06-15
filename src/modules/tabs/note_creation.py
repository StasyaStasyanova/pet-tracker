import flet as ft
from modules.models.note import Note
from modules.models.pet import Pet
import datetime

from utils import WELLBEING_IMAGES

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
            scroll=ft.ScrollMode.AUTO,
        )
        self.bgcolor = ft.Colors.GREY_800
        self.padding = 20
        self.expand = True
        self.visible = False
        self.top = 0
        self.left = 0
        self.right = 0
        self.bottom = 0

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

        self.energy_dropdown = ft.Dropdown(
            label="Энергичность",
            hint_text="Выберите уровень энергии",
            options=[
                ft.dropdown.Option("Очень вялый"),
                ft.dropdown.Option("Вялый"),
                ft.dropdown.Option("Нормально"),
                ft.dropdown.Option("Активный"),
                ft.dropdown.Option("Очень активный"),
            ],
            width=300,
        )
        
        self.appetite_dropdown = ft.Dropdown(
            label="Аппетит",
            hint_text="Выберите как ест питомец",
            options=[
                ft.dropdown.Option("Отказывается от еды"),
                ft.dropdown.Option("Ест очень плохо"),
                ft.dropdown.Option("Ест нормально"),
                ft.dropdown.Option("Хороший аппетит"),
                ft.dropdown.Option("Отличный аппетит"),
            ],
            width=300,
        )
        
        self.mood_dropdown = ft.Dropdown(
            label="Настроение",
            hint_text="Выберите настроение",
            options=[
                ft.dropdown.Option("Подавленное"),
                ft.dropdown.Option("Грустное"),
                ft.dropdown.Option("Спокойное"),
                ft.dropdown.Option("Хорошее"),
                ft.dropdown.Option("Отличное"),
            ],
            width=300,
        )
        
        self.activity_dropdown = ft.Dropdown(
            label="Активность",
            hint_text="Выберите уровень активности",
            options=[
                ft.dropdown.Option("Спит целый день"),
                ft.dropdown.Option("Мало двигается"),
                ft.dropdown.Option("Умеренная активность"),
                ft.dropdown.Option("Игривый"),
                ft.dropdown.Option("Очень игривый"),
            ],
            width=300,
        )
        
        self.selected_wellbeing = "3"
        self._wellbeing_buttons = []

        def make_wellbeing_btn(level: int):
            is_selected = str(level) == self.selected_wellbeing
            btn = ft.Container(
                content=ft.Image(
                    src=WELLBEING_IMAGES[level],
                    fit=ft.BoxFit.CONTAIN,
                ),
                width=72 if is_selected else 52,
                height=72 if is_selected else 52,
                border_radius=999,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
                on_click=lambda e, l=level: self._on_wellbeing_select(l),
                ink=True,
            )
            return btn

        self._wellbeing_buttons = [make_wellbeing_btn(i) for i in range(1, 6)]

        wellbeing_row = ft.Row(
            controls=self._wellbeing_buttons,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        )
        
        self.pet_dropdown = ft.Dropdown(value=self.current_pet, options=pets_dropdown_options, label="Выберите питомца", disabled=dd_disabled)
        
        self.note_content = ft.TextField(
            label="Дополнительная заметка", 
            multiline=True, 
            hint_text="Добавьте дополнительные детали о состоянии питомца...",
            min_lines=3,
            max_lines=5,
        )
        
        self._detail_content.controls = [
            ft.Text("Создание заметки о питомце", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_100),

            ft.Container(
                content=ft.Column([
                    ft.Text("Общее самочувствие:", size=16,
                            weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE),
                    wellbeing_row,
                ], spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=10,
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                border_radius=10,
            ),
            
            ft.Divider(height=1, color=ft.Colors.GREY_600),

            ft.Text("Детальные параметры:", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_200),
            self.energy_dropdown,
            self.appetite_dropdown,
            self.mood_dropdown,
            self.activity_dropdown,
            
            ft.Divider(height=1, color=ft.Colors.GREY_600),
            
            ft.Text("Дополнительная информация:", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_200),
            self.note_content,
            
            self.pet_dropdown,
            
            ft.Row(
                controls=[
                    ft.Button(
                        content=ft.Text("Создать заметку", size=16),
                        color=ft.Colors.PRIMARY,
                        on_click=self.add_note,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=15,
                        ),
                    ),
                    ft.OutlinedButton(
                        content=ft.Text("Очистить"),
                        on_click=self._clear_form,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=15,
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
        ]
        self.visible = True
        self._page.overlay.append(self)
        self._page.update()
    
    def _on_wellbeing_change(self, e):
        self.selected_wellbeing = e.control.value
        self._page.update()
    
    def _on_wellbeing_select(self, level: int):
        self.selected_wellbeing = str(level)
        for i, btn in enumerate(self._wellbeing_buttons):
            selected = (i + 1) == level
            btn.width = 72 if selected else 52
            btn.height = 72 if selected else 52
            btn.update()

    def _clear_form(self, e=None):
        self.energy_dropdown.value = None
        self.appetite_dropdown.value = None
        self.mood_dropdown.value = None
        self.activity_dropdown.value = None
        self.note_content.value = ""
        self.selected_wellbeing = "3"
        for i, btn in enumerate(self._wellbeing_buttons):
            selected = (i + 1) == 3
            btn.width = 72 if selected else 52
            btn.height = 72 if selected else 52
        self._page.update()

    def add_note(self, e):
        if not self.current_pet:
            self._page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Выберите питомца!"), bgcolor=ft.Colors.RED)
            )
            return
        
        self.current_pet = self.pet_dropdown.value
        pet = Pet.get_by_id(self.current_pet)

        note = Note.create(
            content=self.note_content.value if self.note_content.value else "",
            overall_wellbeing=int(self.selected_wellbeing),
            energy=self.energy_dropdown.value,
            appetite=self.appetite_dropdown.value,
            mood=self.mood_dropdown.value,
            activity=self.activity_dropdown.value,
            pet=pet,
            created_at=datetime.datetime.now()
        )

        from modules.appState import app_state
        app_state.update_lists()

        self._clear_form()
        
        self.create_button_clicked()
        
        self._close()

        self._page.show_dialog(
            ft.SnackBar(
                content=ft.Text(f"Заметка для {pet.name} успешно создана!"),
                bgcolor=ft.Colors.GREEN,
                duration=3000,
            )
        )
        
    def create_button_clicked(self):
        from modules.appState import app_state
        from utils import TABS
        app_state.switch_tab(TABS.NOTES.value)

    def _close(self, e=None):
        self.visible = False
        if self in self._page.overlay:
            self._page.overlay.remove(self)
        self._page.update()