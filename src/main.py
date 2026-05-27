import flet as ft
from modules.tabs import *
from modules.appState import app_state
from modules import database

dark_theme = ft.Theme(
    color_scheme=ft.ColorScheme(
        # --accents → primary action color
        primary="#e5ff00",
        on_primary="#252525",

        # --secondary
        secondary="#dddddd",
        on_secondary="#252525",        # --secondary-contrast

        # --main → surface (cards, dialogs, sheets)
        surface="#252525",
        on_surface="#ffffff",          # --main-contrast

        # --darker-text → muted text on surfaces
        on_surface_variant="#dddddd",

        # --borders
        outline="#3a3a3a",
        outline_variant="#3a3a3a",

        # --footer → tertiary
        tertiary="#818f32",
        on_tertiary="#d4d4d4",         # --footer-text

        # Surface containers (elevations above surface)
        surface_container="#2e2e2e",
        surface_container_high="#333333",
        surface_container_highest="#3a3a3a",
    ),
    appbar_theme=ft.AppBarTheme(
        bgcolor="#252525",             # --header-bg
        color="#ffffff",               # --main-contrast (title/icon color)
    ),
)

light_theme = ft.Theme(
    color_scheme=ft.ColorScheme(
        # --accents → primary action color
        primary="#ffa71a",
        on_primary="#fffdf0",

        # --secondary
        secondary="#422318",
        on_secondary="#fffdf0",        # --secondary-contrast

        # --main → surface (cards, dialogs, sheets)
        surface="#fffdf0",
        on_surface="#482f27",          # --main-contrast

        # --darker-text → muted text on surfaces
        on_surface_variant="#422318",

        # --borders
        outline="#d3d3d3",
        outline_variant="#d3d3d3",

        # --footer → tertiary
        tertiary="#a86739",
        on_tertiary="#6a3d30",         # --footer-text

        # Surface containers (elevations above surface)
        surface_container="#eceada",
        surface_container_high="#e2e0d0",
        surface_container_highest="#d8d6c6",
    ),
    appbar_theme=ft.AppBarTheme(
        bgcolor="#fffdf0",             # --header-bg
        color="#482f27",               # --main-contrast (title/icon color)
    ),
)

def switch_page_theme(page: ft.Page, themeMode: ft.ThemeMode):
    page.theme_mode = themeMode
    page.update()

def main(page: ft.Page):
    page.window.maximized = True
    page.dark_theme = dark_theme
    page.theme = light_theme
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.SURFACE
    database.init_db()
    note_creation_overlay = NoteCreationOverlay(page)
    day_detail_overlay = DayDetailOverlay(page)
    pet_detail_overlay = PetDetailOverlay(page, day_detail_overlay)
    mainTab = MainTab()
    petsTab = PetsTab()
    notesTab = NotesTab()
    calendarTab = CalendarTab(page=page, overlay=day_detail_overlay)
    mainContainer = MainContainer()
    petsContainer = PetsContainer()
    notesContainer = NotesContainer()
    calendarContainer = CalendarContainer(page=page, overlay=day_detail_overlay)
    tabs = ft.Tabs(
        selected_index=0,
        length=4,
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                ft.TabBar(
                    tabs=[
                        mainTab,
                        petsTab,
                        notesTab,
                        calendarTab,
                    ],
                ),
                ft.TabBarView(
                    expand=True,
                    controls=[
                        mainContainer,
                        petsContainer,
                        notesContainer,
                        calendarContainer,
                    ]
                )
            ]
        )
    )
    app_state.tabs = tabs
    app_state.pet_detail_overlay = pet_detail_overlay
    app_state.note_creation_overlay = note_creation_overlay
    app_state.mainTab = mainTab
    app_state.petsTab = petsTab
    app_state.notesTab = notesTab
    app_state.calendarTab = calendarTab
    app_state.mainContainer = mainContainer
    app_state.petsContainer = petsContainer
    app_state.notesContainer = notesContainer
    app_state.calendarContainer = calendarContainer

    page.add(tabs)


ft.run(main)