import flet as ft
from modules.tabs import *
from modules.appState import app_state

def main(page: ft.Page):
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

    page.add(tabs)


ft.app(target=main)