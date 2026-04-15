import flet as ft
from modules.tabs import *
from modules.appState import app_state
from modules import database

def main(page: ft.Page):
    database.init_db()
    pet_detail_overlay = PetDetailOverlay(page)
    note_creation_overlay = NoteCreationOverlay(page)
    tabs = ft.Tabs(
        selected_index=0,
        length=3,
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                ft.TabBar(
                    tabs=[
                        MainTab(),
                        PetsTab(),
                        NotesTab(),
                        CalendarTab(),
                    ],
                ),
                ft.TabBarView(
                    expand=True,
                    controls=[
                        MainContainer(),
                        PetsContainer(),
                        NotesContainer(),
                        CalendarContainer(),
                    ]
                )
            ]
        )
    )
    app_state.tabs = tabs
    app_state.pet_detail_overlay = pet_detail_overlay
    app_state.note_creation_overlay = note_creation_overlay

    page.add(tabs)


ft.run(main)