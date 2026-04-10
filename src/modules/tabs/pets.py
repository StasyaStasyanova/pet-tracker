import flet as ft
from datetime import datetime
import os
import shutil
from modules.models.pet import Pet


def calculate_age(birthday):
    today = datetime.now().date()
    if isinstance(birthday, datetime):
        birthday = birthday.date()
    age = today.year - birthday.year
    if today.month < birthday.month or (today.month == birthday.month and today.day < birthday.day):
        age -= 1
    return age

def name_year(age):
    last_digit = age % 10
    if 11 <= age <= 14:
        return "лет"
    
    if last_digit == 1:
        return "год"
    elif 2 <= last_digit <= 4:
        return "года"
    else:
        return "лет"
    

class PetsTab(ft.Tab):
    def __init__(self):
        super().__init__()
        self.label = "Питомцы"


class PetsContainer(ft.Container):
    def __init__(self):
        super().__init__()
        self.pets_list = ft.Column()

        self.file_picker = ft.FilePicker(on_upload=self._on_file_selected)
        self.date_picker = ft.DatePicker(
            first_date=datetime(year=1900, month=1, day=1),
            last_date=datetime.now(),
        )
        self._selected_image_path = None

        self.content = ft.Column([
            ft.Text("Питомцы", size=30, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton(
                "Добавить питомца",
                on_click=self.open_add_dialog,
                icon=ft.Icons.PETS,
            ),
            self.pets_list,
        ])
        self.alignment = ft.Alignment.TOP_CENTER
        self.expand = True

    def did_mount(self):
        self.page.overlay.append(self.date_picker)
        self.load_pets()
        return super().did_mount()

    def load_pets(self):
        self.pets_list.controls.clear()
        pets = Pet.select()

        if not pets:
            self.pets_list.controls.append(
                ft.Text("Нет добавленных питомцев", italic=True, color=ft.Colors.GREY)
            )
        else:
            for pet in pets:
                has_image = pet.image and os.path.exists(pet.image)
                self.pets_list.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Image(
                                src=pet.image,
                                width=80,
                                height=80,
                                fit=ft.BoxFit.COVER,
                                border_radius=10,
                            ) if has_image else ft.Icon(ft.Icons.PETS, size=40),
                            ft.Column([
                                ft.Text(f"{pet.name}", weight=ft.FontWeight.BOLD),
                                ft.Text(f"{pet.AnimalType}"),
                                ft.Text(f"{calculate_age(pet.birthday)} {name_year(calculate_age(pet.birthday))}"),
                            ], spacing=2),
                        ]),
                        padding=10,
                        border=ft.border.all(1, ft.Colors.GREY_400),
                        border_radius=10,
                        margin=ft.margin.only(bottom=5),
                    )
                )

        if self.page:
            self.pets_list.update()

    def _on_file_selected(self, e: list[ft.FilePickerFile]):
        if e:
            self._selected_image_path = e[0].path
            if self._image_path_display:
                self._image_path_display.value = os.path.basename(self._selected_image_path)
                self._image_path_display.color = ft.Colors.GREEN
                self._image_path_display.italic = False
                self._image_path_display.update()

    def open_add_dialog(self, e):
        self._selected_image_path = None

        name_field = ft.TextField(label="Имя", width=300)
        animal_type_field = ft.TextField(label="Тип животного", width=300)

        date_display = ft.Text("Не выбрана", italic=True, color=ft.Colors.GREY)
        self._image_path_display = ft.Text("Файл не выбран", italic=True, color=ft.Colors.GREY)

        def on_date_change(e):
            if self.date_picker.value:
                # TODO: Изменить тайм зону для всех дат в дейтпикере в принципе
                date_display.value = self.date_picker.value.astimezone().strftime("%d.%m.%Y")
                date_display.color = ft.Colors.BLACK
                date_display.italic = False
            else:
                date_display.value = "Не выбрана"
            date_display.update()

        self.date_picker.on_change = on_date_change

        def pick_date(e):
            self.date_picker.open = True
            self.page.update()

        async def pick_file(e):
            files = await self.file_picker.pick_files(
                allowed_extensions=["jpg", "jpeg", "png", "gif", "bmp"],
                dialog_title="Выберите фото питомца",
            )
            self._on_file_selected(files)

        dialog = ft.AlertDialog(
            title=ft.Text("Добавить питомца", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    name_field,
                    ft.Text("Дата рождения:", weight=ft.FontWeight.W_500),
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.CALENDAR_MONTH,
                            on_click=pick_date,
                            tooltip="Выбрать дату",
                        ),
                        date_display,
                    ]),
                    animal_type_field,
                    ft.Divider(),
                    ft.Text("Фото питомца:", weight=ft.FontWeight.W_500),
                    ft.Row([
                        ft.ElevatedButton(
                            "Выбрать фото",
                            on_click=pick_file,
                            icon=ft.Icons.UPLOAD_FILE,
                        ),
                        self._image_path_display,
                    ]),
                ], spacing=15),
                width=400,
                padding=20,
            ),
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: self.close_dialog(dialog)),
                ft.ElevatedButton(
                    "Сохранить",
                    on_click=lambda e: self.save_pet(
                        name_field.value,
                        self.date_picker.value,
                        animal_type_field.value,
                        self._selected_image_path,
                        dialog,
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def close_dialog(self, dialog):
        dialog.open = False
        self._image_path_display = None
        self.page.update()

    def save_pet(self, name, birthday, animal_type, image_path, dialog):
        if not name:
            self.show_snackbar("Введите имя питомца")
            return
        if not birthday:
            self.show_snackbar("Выберите дату рождения")
            return
        if not animal_type:
            self.show_snackbar("Введите тип животного")
            return

        saved_image_path = ""
        if image_path and os.path.exists(image_path):
            images_dir = os.path.join(
                os.getenv("FLET_APP_STORAGE_DATA", "uploads"), "pet_images"
            )
            os.makedirs(images_dir, exist_ok=True)
            ext = os.path.splitext(image_path)[1]
            unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{name}{ext}"
            saved_image_path = os.path.join(images_dir, unique_filename)
            shutil.copy2(image_path, saved_image_path)

        try:
            Pet.create(
                name=name,
                birthday=birthday,
                AnimalType=animal_type,
                image=saved_image_path,
            )
            self.show_snackbar("Питомец успешно добавлен!", True)
            dialog.open = False
            self._image_path_display = None
            self.page.update()
            self.load_pets()
        except Exception as ex:
            self.show_snackbar(f"Ошибка при сохранении: {str(ex)}")

    def show_snackbar(self, message, is_success=False):
        snackbar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.Colors.GREEN if is_success else ft.Colors.RED,
            duration=3000,
        )
        self.page.overlay.append(snackbar)
        snackbar.open = True
        self.page.update()