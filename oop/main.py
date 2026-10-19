import os
from datetime import datetime
import flet as ft
from custom_map import MyCustomMap
from logics import (
    BaseFormatter,
    SnakeCaseFormatter,
    CleanSpaceFormatter,
    SwapCaseFormatter,
    CipherFormatter,
    CensorFormatter
)
class UserConfig:
    def __init__(self, name: str):
        self.name = name
#окно авторизации
class LoginWindow(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.margin = 10
        self.padding = 20
        self.border = ft.border.all(width=1, color=ft.colors.RED_800)
        self.alignment = ft.alignment.center
        self.width = 340
        self.title_text = ft.Text("Welcome", size=20, weight="bold")
        self.login_field = ft.TextField(hint_text="Username / Login")
        self.password_field = ft.TextField(password=True, hint_text="Password")
        self.login_btn = ft.ElevatedButton("Login", on_click=self.login_event)
        self.content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
            controls=[
                self.title_text,
                ft.Column([ft.Text("Логин:", weight="bold", size=12), self.login_field], spacing=4),
                ft.Column([ft.Text("Пароль:", weight="bold", size=12), self.password_field], spacing=4),
                self.login_btn
            ]
        )
    def login_event(self, e):
        if self.login_field.value and self.password_field.value == "999999999":
            saved_user = self.login_field.value
            self.page.controls.clear()
            self.page.add(MainWindow(self.page, saved_user))
            self.page.update()
        else:
            snack = ft.SnackBar(ft.Text("Неверный логин или пароль!"), open=True)
            self.page.overlay.append(snack)
            self.page.update()
#рабочее окно
class MainWindow(ft.Container):
    def __init__(self, page, username):
        super().__init__()
        self.page = page
        self.username = username
        self.time_in = datetime.now()
        self.margin, self.padding = 10, 10
        self.alignment = ft.alignment.center
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.my_map = MyCustomMap()
        self.my_map.put("snake_case", SnakeCaseFormatter("Snake"))
        self.my_map.put("Удалить пробелы", CleanSpaceFormatter("Spaces"))
        self.my_map.put("Исправить Caps Lock", SwapCaseFormatter("Caps"))
        self.my_map.put("Шифрование", CipherFormatter("Cipher"))
        self.my_map.put("Цензура слов", CensorFormatter("Censor"))
        self.users_list = [UserConfig(f"User_{i}") for i in range(10)]
        self.lbl_title = MyTextTitle(f"Welcome, {self.username}!", size=16, weight="bold")
        self.txt_in = MyTextFieldIn(label="Исходный текст", multiline=True, min_lines=2)
        self.txt_out = MyTextFieldOut(label="Результат", multiline=True, min_lines=2, read_only=True)
        self.param_field = MyParamField(label="Параметр (Сдвиг/Слово)", width=170, visible=False)
        self.chk_time = MyCheckbox(label="Добавить время обработки")
        self.lbl_stats = MyLabelStats("Статистика: Слов: 0 | Символов: 0", color="green700")
        self.dropdown_mode = MyDropdown(
            label="Операция", width=220, value="snake_case",
            options=[
                ft.dropdown.Option("snake_case"),
                ft.dropdown.Option("Удалить пробелы"),
                ft.dropdown.Option("Исправить Caps Lock"),
                ft.dropdown.Option("Шифрование"),
                ft.dropdown.Option("Цензура слов")
            ],
            on_change=self.toggle_param
        )
        self.btn_start = MyBtnStart("Запуск", icon=ft.icons.PLAY_ARROW, on_click=self.process)
        self.btn_copy = MyBtnCopy("Копировать", icon=ft.icons.COPY, on_click=self.copy)
        self.btn_clear = MyBtnClear("Очистить", on_click=self.clear)
        self.btn_exit = MyBtnExit("Выход и отчет", color="red", on_click=self.exit_app)
        self.content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            controls=[
                self.lbl_title,
                self.txt_in,
                ft.Row(alignment="center", controls=[self.dropdown_mode, self.param_field]),
                self.chk_time,
                ft.Row(alignment="center", controls=[self.btn_start, self.btn_copy, self.btn_clear]),
                ft.Divider(),
                self.txt_out,
                ft.Row(alignment="spaceBetween", controls=[self.lbl_stats, self.btn_exit])
            ]
        )
    def toggle_param(self, e):
        selected_mode = self.dropdown_mode.value
        if selected_mode == "Цензура слов" or selected_mode == "Шифрование":
            self.param_field.visible = True
        else:
            self.param_field.visible = False
        self.page.update()
    def process(self, e):
        text_data = self.txt_in.value
        if not text_data:
            return
        mode = self.dropdown_mode.value
        param = self.param_field.value
        formatter = self.my_map.get(mode)
        if formatter:
            res = formatter.format_text(text_data, param)
            if self.chk_time.value == True:
                res += f"\n\n[Время: {datetime.now().strftime('%H:%M:%S')}]"
            self.txt_out.value = res
            words = BaseFormatter.count_words(text_data)
            self.lbl_stats.value = f"Статистика: Слов: {words} | Символов: {formatter.symbols_count}"
            self.page.update()
    def copy(self, e):
        if self.txt_out.value:
            self.page.set_clipboard(self.txt_out.value)
            snack = ft.SnackBar(ft.Text("Скопировано в буфер ПК!"), open=True)
            self.page.overlay.append(snack)
            self.page.update()
    def clear(self, e):
        self.txt_in.value = ""
        self.txt_out.value = ""
        self.param_field.value = ""
        self.page.update()
    def exit_app(self, e):
        time_out = datetime.now()
        fmt = "%d.%m.%Y %H:%M:%S"
        grid = (
            f"+--------------------+---------------------+---------------------+\n"
            f"| login              | time_in             | time_out            |\n"
            f"+--------------------+---------------------+---------------------+\n"
            f"| {self.username:<18} | {self.time_in.strftime(fmt)} | {time_out.strftime(fmt)} |\n"
            f"+--------------------+---------------------+---------------------+\n"
        )
        with open("app_report.txt", "w", encoding="utf-8") as f:
            f.write(grid)
        try:
            self.page.window.close()
        except:
            self.page.window_close()

class MyTextTitle(ft.Text): pass
class MyLabelStats(ft.Text): pass
class MyTextFieldIn(ft.TextField): pass
class MyTextFieldOut(ft.TextField): pass
class MyParamField(ft.TextField): pass
class MyDropdown(ft.Dropdown): pass
class MyCheckbox(ft.Checkbox): pass
class MyBtnStart(ft.ElevatedButton): pass
class MyBtnCopy(ft.ElevatedButton): pass
class MyBtnClear(ft.OutlinedButton): pass
class MyBtnExit(ft.ElevatedButton): pass

def main(page: ft.Page):
    page.title = "Welcome Screen"
    page.window_width = 450
    page.window_height = 620
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(LoginWindow(page))

if __name__ == "__main__":
    ft.app(target=main)
