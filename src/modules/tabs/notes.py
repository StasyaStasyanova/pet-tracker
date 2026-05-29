import datetime
import flet as ft
from ..models.note import Note
from ..models.pet import Pet
from utils import WELLBEING_COLORS

class NotesTab(ft.Tab):
    def __init__(self):
        super().__init__()
        self.label = "Заметки"

class NotesContainer(ft.Container):
    def __init__(self):
        super().__init__()
        self.load_notes()

    def notes_button_clicked(self):
        from modules.appState import app_state
        app_state.note_creation_overlay.show_note()

    def load_notes(self):
        notes = Note.select().order_by(Note.created_at.desc())

        if not notes.exists():
            content = ft.Column(
                controls=[
                    ft.Text(
                        "Нет заметок",
                        size=16,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                    ft.Button(content=ft.Text("Добавить заметку"), color=ft.Colors.PRIMARY, on_click=self.notes_button_clicked),
                ],
            )
        else:
            content = ft.Column(
                controls=[
                    ft.Button(content=ft.Text("Добавить заметку"), color=ft.Colors.PRIMARY, on_click=self.notes_button_clicked),
                    ft.ListView(
                        controls=[NoteDisplay(note) for note in notes],
                        spacing=10,
                        padding=ft.padding.all(16),
                        expand=True,
                    ),
                ],
            )

        self.content = content
        self.expand = True

class NoteDisplay(ft.Container):
    def __init__(self, note: Note):
        super().__init__()
        self.note = note

        dots = ft.Row(
            controls=[
                ft.Container(
                    width=10,
                    height=10,
                    border_radius=5,
                    bgcolor=WELLBEING_COLORS.get(note.overall_wellbeing, ft.Colors.GREEN_400)
                    if i < note.overall_wellbeing
                    else ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                )
                for i in range(5)
            ],
            spacing=4,
        )

        header = ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(
                            f"{note.pet.name} · {note.created_at.strftime('%d %b %Y, %H:%M')}",
                            size=13,
                            color=ft.Colors.ON_SURFACE_VARIANT,
                            expand=True,
                        ),
                        ft.Row(
                            controls=[
                                ft.Text("Самочувствие", size=13, color=ft.Colors.ON_SURFACE_VARIANT),
                                dots,
                                ft.Text(
                                    f"{note.overall_wellbeing}/5",
                                    size=13,
                                    weight=ft.FontWeight.W_500,
                                    color=ft.Colors.ON_SURFACE,
                                ),
                            ],
                            spacing=8,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    expand=True,
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_size=30,
                    icon_color=ft.Colors.ERROR,
                    tooltip="Удалить заметку",
                    on_click=self.delete_button_clicked,
                ),
            ],
            spacing=4,
        )
        

        def stat_tile(label: str, value: str | None):
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(label.upper(), size=11, color=ft.Colors.ON_SURFACE_VARIANT),
                        ft.Text(value or "—", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.ON_SURFACE),
                    ],
                    spacing=3,
                ),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                border_radius=8,
                padding=ft.padding.symmetric(horizontal=12, vertical=10),
                expand=True,
            )

        grid = ft.Column(
            controls=[
                ft.Row(controls=[stat_tile("Энергичность", note.energy), stat_tile("Аппетит", note.appetite)], spacing=10),
                ft.Row(controls=[stat_tile("Настроение", note.mood), stat_tile("Активность", note.activity)], spacing=10),
            ],
            spacing=10,
        )

        note_content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Дополнительная заметка", size=11, color=ft.Colors.ON_SURFACE_VARIANT),
                    ft.Text(note.content or "", size=14, color=ft.Colors.ON_SURFACE),
                ],
                spacing=4,
            ),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=12, vertical=10),
            visible=bool(note.content),
        )

        self.content = ft.Column(
            controls=[
                header,
                ft.Divider(height=1, color=ft.Colors.OUTLINE),
                grid,
                note_content,
            ],
            spacing=14,
        )
        self.bgcolor = ft.Colors.SURFACE_CONTAINER
        self.border_radius = 16
        self.border = ft.border.all(1, ft.Colors.OUTLINE)
        self.padding = ft.padding.all(16)
        
    def delete_button_clicked(self, e):
        from modules.appState import app_state
        def close_dialog(e):
            e.page.pop_dialog()
            e.page.update()
        
        def confirm_delete(e):
            self.note.delete_instance()
            
            app_state.update_lists()
            close_dialog(e)
            e.page.update()
            
            e.page.show_dialog(
                ft.SnackBar(
                    content=ft.Text(f"Заметка удалена"),
                    bgcolor=ft.Colors.PRIMARY,
                    duration=3000,
                )
            )
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Удаление заметки"),
            content=ft.Text("Вы уверены, что хотите удалить эту заметку? Это действие нельзя отменить."),
            actions=[
                ft.TextButton("Отмена", on_click=close_dialog),
                ft.ElevatedButton(
                    "Удалить", 
                    on_click=confirm_delete,
                    bgcolor=ft.Colors.ERROR,
                    color=ft.Colors.ON_ERROR,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        e.page.show_dialog(dialog)