import flet as ft
import os
import datetime
import calendar
from modules.models.pet import Pet
from modules.models.note import Note
from .pets import calculate_age, name_year
from modules.appState import app_state
from utils import TABS, WELLBEING_IMAGES, WELLBEING_COLORS
from .calendar import DayDetailOverlay

WELLBEING_TEXT_COLORS = {
    1: ft.Colors.WHITE,
    2: ft.Colors.WHITE,
    3: ft.Colors.WHITE,
    4: ft.Colors.WHITE,
    5: "#2C2C2A",
}


CELL_SIZE = 72

WEEKDAYS_RU = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
MONTHS_RU = ["Январь","Февраль","Март","Апрель","Май","Июнь",
             "Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"]


class PetDetailOverlay(ft.Container):
    def __init__(self, page: ft.Page, day_detail_overlay: DayDetailOverlay):
        super().__init__()
        self._page = page
        self.pet = None
        self._ddoverlay = day_detail_overlay
        self._today = datetime.date.today()
        self._current_month = self._today.replace(day=1)

        self._avatar = ft.Container(
            width=72, height=72, border_radius=36,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
        )
        self._name = ft.Text("", size=20, weight=ft.FontWeight.W_500,
                             color=ft.Colors.ON_SURFACE)
        self._subtitle = ft.Text("", size=13, color=ft.Colors.ON_SURFACE_VARIANT)
        self._birthday_chip = ft.Container(
            content=ft.Text("", size=11, color=ft.Colors.ON_SURFACE_VARIANT),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            border_radius=20,
            padding=ft.Padding.symmetric(horizontal=10, vertical=3),
        )

        profile_row = ft.Row(
            controls=[
                self._avatar,
                ft.Column(
                    controls=[
                        self._name,
                        self._subtitle,
                        ft.Row(controls=[self._birthday_chip], spacing=6),
                    ],
                    spacing=4,
                    expand=True,
                ),
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=ft.Colors.ON_SURFACE_VARIANT,
                    on_click=lambda e: self._close(),
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=16,
        )

        self._month_label = ft.Text("", size=13, weight=ft.FontWeight.W_500,
                                    color=ft.Colors.ON_SURFACE)
        self._cal_grid = ft.Column(spacing=3)

        calendar_section = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("История самочувствия", size=11,
                            color=ft.Colors.ON_SURFACE_VARIANT),
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.CHEVRON_LEFT,
                                icon_size=16,
                                icon_color=ft.Colors.ON_SURFACE_VARIANT,
                                on_click=lambda e: self._change_month(-1),
                            ),
                            self._month_label,
                            ft.IconButton(
                                icon=ft.Icons.CHEVRON_RIGHT,
                                icon_size=16,
                                icon_color=ft.Colors.ON_SURFACE_VARIANT,
                                on_click=lambda e: self._change_month(1),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Text(d, size=10,
                                               color=ft.Colors.ON_SURFACE_VARIANT,
                                               text_align=ft.TextAlign.CENTER),
                                expand=True,
                            )
                            for d in WEEKDAYS_RU
                        ],
                        spacing=3,
                    ),
                    self._cal_grid,
                ],
                spacing=8,
            ),
            padding=ft.Padding.symmetric(horizontal=0, vertical=4),
        )

        add_btn = ft.Container(
            content=ft.TextButton(
                content="+ Добавить заметку",
                style=ft.ButtonStyle(color=ft.Colors.PRIMARY),
                on_click=self._notes_button_clicked,
            ),
            alignment=ft.Alignment.CENTER,
        )

        inner_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(content=profile_row,
                                 padding=ft.Padding.all(20),
                                 border=ft.Border.only(
                                     bottom=ft.BorderSide(1, ft.Colors.OUTLINE))),
                    ft.Container(content=calendar_section,
                                 padding=ft.Padding.symmetric(horizontal=20, vertical=12),
                                 border=ft.Border.only(
                                     bottom=ft.BorderSide(1, ft.Colors.OUTLINE))),
                    ft.Container(content=add_btn,
                                 padding=ft.Padding.symmetric(horizontal=20, vertical=12)),
                ],
                spacing=0,
            ),
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            border_radius=16,
            border=ft.Border.all(1, ft.Colors.OUTLINE),
            width=600,
        )

        self.content = ft.Column(
            controls=[inner_card],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.bgcolor = ft.Colors.SURFACE
        self.padding = ft.Padding.all(20)
        self.expand = True
        self.visible = False
        self.top = 0
        self.left = 0
        self.right = 0
        self.bottom = 0

    def _legend(self):
        items = []
        for level, color in WELLBEING_COLORS.items():
            items.append(
                ft.Row(
                    controls=[
                        ft.Container(width=8, height=8, border_radius=4, bgcolor=color),
                        ft.Text(str(level), size=11, color=ft.Colors.ON_SURFACE_VARIANT),
                    ],
                    spacing=4,
                    tight=True,
                )
            )
        items[-1].controls.append(
            ft.Text(" — самочувствие", size=11, color=ft.Colors.ON_SURFACE_VARIANT)
        )
        return ft.Row(controls=items, spacing=10, wrap=True)
    
    def _on_day_clicked(self, date: datetime.date):
        self._ddoverlay.show(date, self.pet)

    def _build_calendar(self):
        if not self.pet:
            return
        year, month = self._current_month.year, self._current_month.month
        self._month_label.value = f"{MONTHS_RU[month - 1]} {year}"

        start = datetime.datetime(year, month, 1)
        end = datetime.datetime(year, month,
                                calendar.monthrange(year, month)[1], 23, 59, 59)
        notes = list(
            Note.select()
            .where(Note.pet == self.pet,
                Note.created_at >= start,
                Note.created_at <= end)
        )
        notes_by_day = {}
        for n in notes:
            notes_by_day.setdefault(n.created_at.day, []).append(n)

        CIRCLE_SIZE = 52

        rows = []
        for week in calendar.monthcalendar(year, month):
            cells = []
            for day in week:
                if day == 0:
                    cells.append(ft.Container(expand=True))
                    continue

                day_notes = notes_by_day.get(day, [])
                date = datetime.date(year, month, day)
                is_today = date == self._today
                avg_well = (sum(n.overall_wellbeing for n in day_notes)
                            // len(day_notes)) if day_notes else None

                if avg_well:
                    circle = ft.Container(
                        content=ft.Image(
                            src=WELLBEING_IMAGES[avg_well],
                            width=CIRCLE_SIZE,
                            height=CIRCLE_SIZE,
                            fit=ft.BoxFit.COVER,
                        ),
                        width=CIRCLE_SIZE,
                        height=CIRCLE_SIZE,
                        border_radius=CIRCLE_SIZE // 2,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        border=ft.Border.all(2, "#e5ff00") if is_today else None,
                    )
                else:
                    circle = ft.Container(
                        width=CIRCLE_SIZE,
                        height=CIRCLE_SIZE,
                        border_radius=CIRCLE_SIZE // 2,
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                        border=ft.Border.all(2, "#e5ff00") if is_today else None,
                    )

                cell = ft.Container(
                    content=ft.Column(
                        controls=[
                            circle,
                            ft.Text(
                                str(day),
                                size=11,
                                color=ft.Colors.ON_SURFACE_VARIANT,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                        tight=True,
                    ),
                    on_click=lambda e, d=date: self._on_day_clicked(d),
                    expand=True,
                    alignment=ft.Alignment.TOP_CENTER,
                )
                cells.append(cell)

            rows.append(ft.Row(controls=cells, spacing=4, alignment=ft.MainAxisAlignment.SPACE_BETWEEN))

        self._cal_grid.controls = rows

    def _change_month(self, direction: int):
        m = self._current_month.month + direction
        y = self._current_month.year
        if m > 12:
            m, y = 1, y + 1
        elif m < 1:
            m, y = 12, y - 1
        self._current_month = datetime.date(y, m, 1)
        self._build_calendar()
        self._month_label.update()
        self._cal_grid.update()

    def _notes_button_clicked(self, e=None):
        app_state.note_creation_overlay.show_note(self.pet)
        self._close()

    def show_pet(self, pet: Pet):
        self.pet = pet
        self._current_month = self._today.replace(day=1)
        has_image = pet.image and os.path.exists(pet.image)

        self._avatar.content = (
            ft.Image(src=pet.image, width=72, height=72, fit=ft.BoxFit.COVER)
            if has_image
            else ft.Icon(ft.Icons.PETS, size=36, color=ft.Colors.PRIMARY)
        )
        self._name.value = pet.name
        self._subtitle.value = (
            f"{pet.AnimalType} · "
            f"{calculate_age(pet.birthday)} {name_year(calculate_age(pet.birthday))}"
        )
        self._birthday_chip.content.value = f"День рождения: {str(pet.birthday)[:10]}"

        self._build_calendar()

        self.visible = True
        if self not in self._page.overlay:
            self._page.overlay.append(self)
        self._page.update()

    def _close(self):
        self.visible = False
        if self in self._page.overlay:
            self._page.overlay.remove(self)
        self._page.update()