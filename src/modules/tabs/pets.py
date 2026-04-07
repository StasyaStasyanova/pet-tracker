import flet as ft
import datetime
import os
import shutil
from modules.models.pet import Pet

class PetsTab(ft.Tab):
    def __init__(self):
        super().__init__()
        self.label = "Питомцы"

class PetsContainer(ft.Container):
    def __init__(self):
        super().__init__()
#         self.pets_list = ft.Column()
#         self.load_pets()
        
#         self.content = ft.Column([
#             ft.Text("Питомцы", size=30, weight=ft.FontWeight.BOLD),
#             ft.ElevatedButton(
#                 "Добавить питомца",
#                 on_click=self.open_add_dialog,
#                 icon=ft.icons.PETS
#             ),
#             self.pets_list
#         ])
#         self.alignment = ft.Alignment.TOP_CENTER
#         self.expand = True
    
#     def load_pets(self):
#         """Загрузка списка питомцев из БД"""
#         self.pets_list.controls.clear()
#         pets = Pet.select()
        
#         if not pets:
#             self.pets_list.controls.append(
#                 ft.Text("Нет добавленных питомцев", italic=True, color=ft.Colors.GREY)
#             )
#         else:
#             for pet in pets:
#                 self.pets_list.controls.append(
#                     ft.Container(
#                         content=ft.Row([
#                             ft.Image(
#                                 src=pet.image if os.path.exists(pet.image) else None,
#                                 width=50,
#                                 height=50,
#                                 fit=ft.ImageFit.COVER,
#                                 border_radius=25,
#                             ) if pet.image and os.path.exists(pet.image) else ft.Icon(ft.icons.PETS, size=40),
#                             ft.Column([
#                                 ft.Text(f"Имя: {pet.name}", weight=ft.FontWeight.BOLD),
#                                 ft.Text(f"Тип: {pet.AnimalType}"),
#                                 ft.Text(f"Возраст: {pet.age} лет"),
#                             ], spacing=2),
#                         ]),
#                         padding=10,
#                         border=ft.border.all(1, ft.Colors.GREY_400),
#                         border_radius=10,
#                         margin=ft.margin.only(bottom=5),
#                     )
#                 )
#         self.pets_list.update()
    
#     def open_add_dialog(self, e):
#         name_field = ft.TextField(label="Имя", width=300)

#         selected_date = ft.Ref[ft.Text]()
#         date_picker = ft.DatePicker(
#             on_change=lambda e: selected_date.current.update(),
#             first_date=datetime(year=1900, month=1, day=1),
#             last_date=datetime.now(),
#         )
        
#         date_display = ft.Text(
#             "Не выбрана",
#             ref=selected_date,
#             italic=True,
#             color=ft.Colors.GREY
#         )
        
#         def pick_date(e):
#             page = self.page
#             page.overlay.append(date_picker)
#             page.update()
#             date_picker.open()
        
#         def update_date_display(e):
#             if date_picker.value:
#                 date_display.value = date_picker.value.strftime("%d.%m.%Y")
#                 date_display.color = ft.Colors.BLACK
#                 date_display.italic = False
#                 age = calculate_age(date_picker.value)
#                 age_field.value = str(age)
#                 age_field.update()
#             else:
#                 date_display.value = "Не выбрана"
#                 age_field.value = ""
#             date_display.update()
        
#         date_picker.on_change = update_date_display
        
#         age_field = ft.TextField(
#             label="Возраст (лет)",
#             width=150,
#             hint_text="Рассчитывается автоматически"
#         )

#         animal_type_field = ft.TextField(label="Тип животного", width=300)
        
#         selected_image_path = ft.Ref[ft.Text]()
#         file_picker = ft.FilePicker()
        
#         def pick_file(e):
#             file_picker.pick_files(
#                 allowed_extensions=["jpg", "jpeg", "png", "gif", "bmp"],
#                 dialog_title="Выберите фото питомца"
#             )
        
#         def on_file_selected(e: ft.FilePickerUploadEvent):
#             if e.files:
#                 file_path = e.files[0].path
#                 image_path_display.value = os.path.basename(file_path)
#                 image_path_display.color = ft.Colors.GREEN
#                 image_path_display.update()
#                 file_picker.selected_path = file_path
        
#         file_picker.on_upload = on_file_selected
        
#         image_path_display = ft.Text(
#             "Файл не выбран",
#             ref=selected_image_path,
#             italic=True,
#             color=ft.Colors.GREY
#         )

#         dialog = ft.AlertDialog(
#             title=ft.Text("Добавить питомца", size=20, weight=ft.FontWeight.BOLD),
#             content=ft.Container(
#                 content=ft.Column([
#                     name_field,
#                     ft.Text("Дата рождения:", weight=ft.FontWeight.W_500),
#                     ft.Row([
#                         ft.IconButton(icon=ft.icons.CALENDAR_MONTH, on_click=pick_date, tooltip="Выбрать дату"),
#                         date_display,
#                     ]),
#                     ft.Row([
#                         age_field,
#                         ft.Text("(рассчитывается автоматически при выборе даты)", italic=True, size=11),
#                     ]),
#                     animal_type_field,
#                     ft.Divider(),
#                     ft.Text("Фото питомца:", weight=ft.FontWeight.W_500),
#                     ft.Row([
#                         ft.ElevatedButton(
#                             "Выбрать фото",
#                             on_click=pick_file,
#                             icon=ft.icons.UPLOAD_FILE,
#                         ),
#                         image_path_display,
#                     ]),
#                 ], spacing=15),
#                 width=400,
#                 padding=20,
#             ),
#             actions=[
#                 ft.TextButton("Отмена", on_click=lambda e: self.close_dialog(dialog)),
#                 ft.ElevatedButton("Сохранить", on_click=lambda e: self.save_pet(
#                     name_field.value,
#                     date_picker.value,
#                     age_field.value,
#                     animal_type_field.value,
#                     file_picker.selected_path if hasattr(file_picker, 'selected_path') else None,
#                     dialog
#                 )),
#             ],
#             actions_alignment=ft.MainAxisAlignment.END,
#         )
        
#         self.page.overlay.append(file_picker)
#         self.page.dialog = dialog
#         dialog.open = True
#         self.page.update()
    
#     def close_dialog(self, dialog):
#         dialog.open = False
#         self.page.update()
    
#     def save_pet(self, name, birthday, age_str, animal_type, image_path, dialog):
#         if not name:
#             self.show_snackbar("Введите имя питомца")
#             return
#         if not birthday:
#             self.show_snackbar("Выберите дату рождения")
#             return
#         if not animal_type:
#             self.show_snackbar("Введите тип животного")
#             return
        
#         if age_str and age_str.isdigit():
#             age = int(age_str)
#         else:
#             age = calculate_age(birthday)
        
#         saved_image_path = ""
#         if image_path and os.path.exists(image_path):
#             images_dir = os.path.join(os.getenv("FLET_APP_STORAGE_DATA", "uploads"), "pet_images")
#             os.makedirs(images_dir, exist_ok=True)
            
#             ext = os.path.splitext(image_path)[1]
#             unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{name}{ext}"
#             saved_image_path = os.path.join(images_dir, unique_filename)
            
#             shutil.copy2(image_path, saved_image_path)
        
#         try:
#             Pet.create(
#                 name=name,
#                 birthday=birthday,
#                 age=age,
#                 AnimalType=animal_type,
#                 image=saved_image_path
#             )
#             self.show_snackbar("Питомец успешно добавлен!", True)
#             dialog.open = False
#             self.page.update()
#             self.load_pets()
#         except Exception as e:
#             self.show_snackbar(f"Ошибка при сохранении: {str(e)}")
    
#     def show_snackbar(self, message, is_success=False):
#         """Показ уведомления"""
#         snackbar = ft.SnackBar(
#             content=ft.Text(message),
#             bgcolor=ft.Colors.GREEN if is_success else ft.Colors.RED,
#             duration=3000,
#         )
#         self.page.overlay.append(snackbar)
#         snackbar.open = True
#         self.page.update()


# def calculate_age(birthday):
#     today = datetime.now().date()
#     if isinstance(birthday, datetime):
#         birthday = birthday.date()
#     age = today.year - birthday.year
#     if today.month < birthday.month or (today.month == birthday.month and today.day < birthday.day):
#         age -= 1
#     return age