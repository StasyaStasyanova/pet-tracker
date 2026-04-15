import flet as ft

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
        )
        self.bgcolor = ft.Colors.GREY_800
        self.padding = 20
        self.expand = True
        self.visible = False

    def show_note(self):
        self._detail_content.controls = [
            ft.Text("Тут можно будет создать заметку", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_100),
        ]
        self.visible = True
        self._page.overlay.append(self)
        self._page.update()

    def _close(self):
        self.visible = False
        self._page.overlay.remove(self)
        self._page.update()