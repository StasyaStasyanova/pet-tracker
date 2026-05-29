import flet as ft
from datetime import datetime
import os
import shutil
from modules.models.pet import Pet
from utils import TABS


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
    
def _on_pet_display_clicked(pet: Pet):
    from modules.appState import app_state
    app_state.pet_detail_overlay.show_pet(pet)

class PetsTab(ft.Tab):
    def __init__(self):
        super().__init__()
        self.label = "Питомцы"

class PetDisplayCompact(ft.Container):
    def __init__(self, pet: Pet, image_size: tuple = (90, 90), width: int = 140, on_click=None):
        super().__init__()
        self.pet = pet

        has_image = self.pet.image and os.path.exists(self.pet.image)

        avatar = ft.Container(
            content=ft.Image(
                src=self.pet.image,
                width=image_size[0],
                height=image_size[1],
                fit=ft.BoxFit.COVER,
            ) if has_image else ft.Icon(ft.Icons.PETS, size=48, color=ft.Colors.PRIMARY),
            width=image_size[0],
            height=image_size[1],
            border_radius=15,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
        )

        self.content = ft.Column(
            controls=[
                avatar,
                ft.Text(
                    pet.name,
                    weight=ft.FontWeight.BOLD,
                    size=18,
                    color=ft.Colors.ON_SURFACE,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.width = width
        self.padding = ft.padding.symmetric(horizontal=20, vertical=16)
        self.bgcolor = ft.Colors.SURFACE_CONTAINER
        self.border_radius = 20
        self.shadow = ft.BoxShadow(
            spread_radius=0,
            blur_radius=16,
            color=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
            offset=ft.Offset(0, 4),
        )
        self.ink = True
        self.on_click = on_click if on_click else lambda e, p=pet: _on_pet_display_clicked(p)

class PetDisplay(ft.Container):
    def __init__(self, pet: Pet, on_click=None):
        super().__init__()
        self.pet = pet

        has_image = self.pet.image and os.path.exists(self.pet.image)

        avatar = ft.Container(
            content=ft.Image(
                src=self.pet.image,
                width=64,
                height=64,
                fit=ft.BoxFit.COVER,
            ) if has_image else ft.Icon(ft.Icons.PETS, size=32, color=ft.Colors.PRIMARY),
            width=64,
            height=64,
            border_radius=32,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
        )

        info = ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(
                            pet.name,
                            weight=ft.FontWeight.BOLD,
                            size=16,
                            color=ft.Colors.ON_SURFACE,
                        ),
                        ft.Text(
                            str(pet.AnimalType),
                            size=12,
                            color=ft.Colors.ON_SURFACE_VARIANT,
                        ),
                        ft.Container(
                            content=ft.Text(
                                f"{calculate_age(self.pet.birthday)} {name_year(calculate_age(self.pet.birthday))}",
                                size=11,
                                color=ft.Colors.PRIMARY,
                                weight=ft.FontWeight.W_500,
                            ),
                            bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.PRIMARY),
                            border_radius=20,
                            padding=ft.padding.symmetric(horizontal=8, vertical=2),
                        ),
                    ],
                    spacing=4,
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_size=30,
                    icon_color=ft.Colors.ERROR,
                    tooltip="Удалить питомца",
                    on_click=self.delete_button_clicked,
                ),
            ],
            spacing=4,
            expand=True,
        ) 

        self.content = ft.Row(
            controls=[avatar, info],
            spacing=14,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.padding = ft.padding.symmetric(horizontal=16, vertical=12)
        self.bgcolor = ft.Colors.SURFACE
        self.border_radius = 16
        self.shadow = ft.BoxShadow(
            spread_radius=0,
            blur_radius=16,
            color=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
            offset=ft.Offset(0, 4),
        )
        self.border = ft.border.all(1, ft.Colors.with_opacity(0.12, ft.Colors.WHITE))
        self.ink = True
        self.on_click = on_click if on_click else lambda e, p=pet: _on_pet_display_clicked(p)
        
    def delete_button_clicked(self, e):
        from modules.appState import app_state
        def close_dialog(e):
            e.page.pop_dialog()
            e.page.update()
        
        def confirm_delete(e):
            self.pet.delete_instance()
            
            app_state.update_lists()
            close_dialog(e)
            e.page.update()
            
            e.page.show_dialog(
                ft.SnackBar(
                    content=ft.Text(f"Питомец удален"),
                    bgcolor=ft.Colors.PRIMARY,
                    duration=3000,
                )
            )
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Удаление питомца"),
            content=ft.Text("Вы уверены, что хотите удалить питомца? Это действие нельзя отменить."),
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
        self.selected_date = datetime.now().date()

        self.content = ft.Column([
            ft.Text("Питомцы", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.ON_SURFACE),
            ft.ElevatedButton(
                "Добавить питомца",
                on_click=self.open_add_dialog,
                icon=ft.Icons.PETS,
                bgcolor=ft.Colors.PRIMARY,
                color=ft.Colors.ON_PRIMARY
            ),
            ft.ListView(controls=self.pets_list,
                        spacing=10,
                        padding=ft.padding.all(16),
                        expand=True,),
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
                ft.Text("Нет добавленных питомцев", italic=True, color=ft.Colors.ON_SURFACE_VARIANT)
            )
        else:
            for pet in pets:
                self.pets_list.controls.append(
                    PetDisplay(pet),
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

        date_display = ft.Text("Не выбрана", italic=True, color=ft.Colors.ON_SURFACE_VARIANT)
        self._image_path_display = ft.Text("Файл не выбран", italic=True, color=ft.Colors.ON_SURFACE_VARIANT, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS, width=200,)

        def on_date_change(e):
            if self.date_picker.value:
                if self.date_picker.value.tzinfo is not None:
                    self.selected_date = self.date_picker.value.astimezone().date()
                else:
                    self.selected_date = self.date_picker.value
                date_display.value = self.selected_date.strftime("%d.%m.%Y")
                date_display.color = ft.Colors.ON_SURFACE
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
                        self.selected_date,
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
            from ..appState import app_state
            app_state.update_lists()
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