import datetime
import calendar
import flet as ft
from ..models.note import Note
from ..models.pet import Pet

WELLBEING_COLORS = {
    1: ft.Colors.RED_400,
    2: ft.Colors.ORANGE_400,
    3: ft.Colors.GREEN_600,
    4: ft.Colors.GREEN_400,
    5: ft.Colors.GREEN_200,
}

WEEKDAYS_RU = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
MONTHS_RU = ["Январь","Февраль","Март","Апрель","Май","Июнь",
             "Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"]

class DayDetailOverlay(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._body = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("", size=16, weight=ft.FontWeight.W_500,
                                    color=ft.Colors.ON_SURFACE, key="title"),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                icon_color=ft.Colors.ON_SURFACE_VARIANT,
                                on_click=self._close,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Divider(height=1, color=ft.Colors.OUTLINE),
                    self._body,
                ],
                spacing=12,
                tight=True,
            ),
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            border_radius=16,
            border=ft.border.all(1, ft.Colors.OUTLINE),
            padding=ft.padding.all(16),
            width=360,
        )
        self.bgcolor = ft.Colors.with_opacity(0.6, ft.Colors.BLACK)
        self.expand = True
        self.alignment = ft.Alignment.CENTER
        self.visible = False

    def _title_text(self):
        return self.content.content.controls[0].controls[0]

    def show(self, date: datetime.date):
        notes = list(
            Note.select()
            .where(
                Note.created_at >= datetime.datetime.combine(date, datetime.time.min),
                Note.created_at <= datetime.datetime.combine(date, datetime.time.max),
            )
            .order_by(Note.created_at)
        )

        self._title_text().value = date.strftime("%d %B %Y")
        self._body.controls = [self._note_card(n) for n in notes] if notes else [
            ft.Text("Нет заметок за этот день", color=ft.Colors.ON_SURFACE_VARIANT, size=14)
        ]

        self.visible = True
        if self not in self._page.overlay:
            self._page.overlay.append(self)
        self._page.update()

    def _note_card(self, note: Note) -> ft.Container:
        dots = ft.Row(
            controls=[
                ft.Container(
                    width=8, height=8, border_radius=4,
                    bgcolor=WELLBEING_COLORS.get(note.overall_wellbeing, ft.Colors.GREEN_400)
                    if i < note.overall_wellbeing
                    else ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                )
                for i in range(5)
            ],
            spacing=3,
        )

        def chip(label, value):
            return ft.Container(
                content=ft.Text(f"{label}: {value or '—'}", size=11,
                                color=ft.Colors.ON_SURFACE_VARIANT),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                border_radius=20,
                padding=ft.padding.symmetric(horizontal=8, vertical=3),
            )

        chips = ft.Row(
            controls=[
                chip("Энергия", note.energy),
                chip("Аппетит", note.appetite),
                chip("Настроение", note.mood),
                chip("Активность", note.activity),
            ],
            wrap=True,
            spacing=4,
            run_spacing=4,
        )

        controls = [
            ft.Row(
                controls=[
                    ft.Text(note.pet.name, size=14, weight=ft.FontWeight.W_500,
                            color=ft.Colors.ON_SURFACE),
                    dots,
                    ft.Text(note.created_at.strftime("%H:%M"), size=12,
                            color=ft.Colors.ON_SURFACE_VARIANT),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            chips,
        ]

        if note.content:
            controls.append(
                ft.Text(note.content, size=13, color=ft.Colors.ON_SURFACE_VARIANT)
            )

        return ft.Container(
            content=ft.Column(controls=controls, spacing=8),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            border_radius=10,
            padding=ft.padding.all(12),
        )
    def _close(self, e):
        self.visible = False
        self._page.overlay.remove(self)
        self._page.update()

class CalendarDay(ft.Container):
    def __init__(self, day: int, is_current_month: bool, is_today: bool,
                 notes: list, on_click):
        super().__init__()
        self._notes = notes

        dots = ft.Row(
            controls=[
                ft.Container(
                    width=7, height=7, border_radius=4,
                    bgcolor=WELLBEING_COLORS.get(n.overall_wellbeing, ft.Colors.GREEN_400),
                )
                for n in notes[:5]
            ],
            spacing=3,
            wrap=True,
        )
        if not dots.controls:
            dots.controls.append(ft.Container(width=7, height=7, border_radius=4, bgcolor=ft.Colors.TRANSPARENT))

        self.content = ft.Column(
            controls=[
                ft.Text(
                    str(day),
                    size=13,
                    weight=ft.FontWeight.W_500,
                    color=ft.Colors.ON_SURFACE if is_current_month
                    else ft.Colors.with_opacity(0.35, ft.Colors.ON_SURFACE),
                ),
                dots,
            ],
            spacing=4,
            tight=True,
        )
        self.bgcolor = ft.Colors.SURFACE_CONTAINER
        self.border_radius = 8
        self.border = ft.border.all(
            2 if is_today else 1,
            "#e5ff00" if is_today else ft.Colors.OUTLINE,
        )
        self.padding = ft.padding.all(8)
        self.on_click = on_click
        self.ink = True
        self.opacity = 1.0 if is_current_month else 0.4

    def _close(self, e):
        self.visible = False
        self._page.overlay.remove(self)
        self._page.update()

class CalendarTab(ft.Tab):
    def __init__(self, page: ft.Page, overlay: DayDetailOverlay):
        super().__init__()
        self.label = "Календарь"
        self.content = CalendarContainer(page=page, overlay=overlay)

class CalendarContainer(ft.Container):
    def __init__(self, page: ft.Page, overlay: DayDetailOverlay):
        super().__init__()
        self._page = page
        self._overlay = overlay
        self._today = datetime.date.today()
        self._current = self._today.replace(day=1)
        self._header = ft.Text("", size=16, weight=ft.FontWeight.W_500,
                               color=ft.Colors.ON_SURFACE)
        self._grid = ft.Column(spacing=4)

        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(ft.Icons.CHEVRON_LEFT,
                                      icon_color=ft.Colors.ON_SURFACE,
                                      on_click=self._prev_month),
                        self._header,
                        ft.IconButton(ft.Icons.CHEVRON_RIGHT,
                                      icon_color=ft.Colors.ON_SURFACE,
                                      on_click=self._next_month),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                d,
                                size=11,
                                color=ft.Colors.ON_SURFACE_VARIANT,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            expand=True,
                        )
                        for d in WEEKDAYS_RU
                    ],
                    spacing=4,
                ),
                self._grid,
            ],
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
        )
        self.padding = ft.padding.all(16)
        self.expand = True
        self._build_month()

    def _build_month(self):
        year, month = self._current.year, self._current.month
        self._header.value = f"{MONTHS_RU[month - 1]} {year}"

        # fetch all notes for this month in one query
        start = datetime.datetime(year, month, 1)
        end = datetime.datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
        notes_this_month = list(Note.select().where(
            Note.created_at >= start,
            Note.created_at <= end,
        ))

        # group by day
        notes_by_day: dict[int, list] = {}
        for n in notes_this_month:
            notes_by_day.setdefault(n.created_at.day, []).append(n)

        cal = calendar.monthcalendar(year, month)
        rows = []
        for week in cal:
            cells = []
            for day in week:
                if day == 0:
                    cells.append(ft.Container(expand=True))  # empty padding cell
                else:
                    date = datetime.date(year, month, day)
                    cells.append(
                        ft.Container(
                            content=CalendarDay(
                                day=day,
                                is_current_month=True,
                                is_today=(date == self._today),
                                notes=notes_by_day.get(day, []),
                                on_click=lambda e, d=date: self._on_day_click(d),
                            ),
                            expand=True,
                        )
                    )
            rows.append(ft.Row(controls=cells, spacing=4, expand=True))

        self._grid.controls = rows

    def _on_day_click(self, date: datetime.date):
        self._overlay.show(date)

    def _prev_month(self, e):
        self._current = (self._current - datetime.timedelta(days=1)).replace(day=1)
        self._build_month()
        self._grid.update()
        self._header.update()

    def _next_month(self, e):
        # jump to next month
        if self._current.month == 12:
            self._current = self._current.replace(year=self._current.year + 1, month=1)
        else:
            self._current = self._current.replace(month=self._current.month + 1)
        self._build_month()
        self._grid.update()
        self._header.update()