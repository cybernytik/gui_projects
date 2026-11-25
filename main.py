import customtkinter as ctk
from tkinter import messagebox
from pathlib import Path

from patients import load_patients, save_patients, validate_patient
from stat_patients import show_statistics


# настройки графического интерфейса
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BG = "#F2F8FC"
PANEL = "#FFFFFF"
ACCENT = "#6BAED6"
TEAL = "#75C6C0"
BUTTON = "#4E91BD"
TEXT = "#243746"
SECONDARY = "#8296A5"
BORDER = "#DCEAF2"
SELECTED = "#E4F2FA"

DATA_FILE = Path(__file__).resolve().parent / "patients.json"

# данные
patients = []
selected_index = None


# главное окно

root = ctk.CTk()
root.title("MEDI DATA — Patient Management")
root.geometry("1100x760")
root.minsize(900, 620)
root.configure(fg_color=BG)


# вспомогательные функции

def persist_patients():
    """сохраняет текущий список пациентов в JSON"""

    try:
        save_patients(DATA_FILE, patients)
        return True

    except (OSError, TypeError, ValueError) as error:
        messagebox.showerror(
            "Ошибка сохранения",
            f"Не удалось сохранить данные:\n{error}",
            parent=root
        )
        return False


def select_patient(index):
    """выбирает пациента в таблице"""

    global selected_index

    selected_index = index
    render_table()


def render_table():
    """обновляет таблицу и счётчик пациентов"""

    for widget in table.winfo_children():
        widget.destroy()

    count_label.configure(
        text=f"Всего пациентов: {len(patients)}"
    )

    if not patients:
        empty_label = ctk.CTkLabel(
            table,
            text="Список пациентов пока пуст",
            font=("Arial", 16),
            text_color=SECONDARY
        )
        empty_label.pack(pady=40)

    else:
        for index, patient in enumerate(patients):

            if index == selected_index:
                row_color = SELECTED
            else:
                row_color = PANEL

            row = ctk.CTkFrame(
                table,
                fg_color=row_color,
                corner_radius=8,
                border_width=1,
                border_color=BORDER
            )

            row.pack(
                fill="x",
                padx=5,
                pady=3
            )

            values = [
                patient["name"],
                str(patient["age"]),
                patient["gender"],
                str(patient["height"]),
                str(patient["weight"]),
                str(patient["bmi"])
            ]

            for column, value in enumerate(values):

                label = ctk.CTkLabel(
                    row,
                    text=value,
                    font=("Arial", 13),
                    text_color=TEXT,
                    anchor="w"
                )

                label.grid(
                    row=0,
                    column=column,
                    sticky="ew",
                    padx=8,
                    pady=12
                )

                label.bind(
                    "<Button-1>",
                    lambda event, i=index: select_patient(i)
                )

            row.bind(
                "<Button-1>",
                lambda event, i=index: select_patient(i)
            )

            for column in range(6):
                row.grid_columnconfigure(
                    column,
                    weight=1
                )

    if selected_index is None or not patients:
        edit_button.configure(state="disabled")
        delete_button.configure(state="disabled")

    else:
        edit_button.configure(state="normal")
        delete_button.configure(state="normal")


def refresh_patients():
    """повторно загружает данные из JSON"""

    global patients, selected_index

    try:
        updated_patients = load_patients(DATA_FILE)

    except (OSError, ValueError, TypeError) as error:
        messagebox.showerror(
            "Ошибка загрузки",
            f"Не удалось прочитать JSON:\n{error}",
            parent=root
        )
        return

    patients = updated_patients
    selected_index = None

    render_table()

# форма добавления и редактирования
def open_patient_form(index=None):
    """открывает форму добавления или редактирования пациента"""

    is_editing = index is not None

    form = ctk.CTkToplevel(root)

    if is_editing:
        form.title("Редактирование пациента")
    else:
        form.title("Добавление пациента")

    form.geometry("430x570")
    form.resizable(False, False)
    form.configure(fg_color=BG)

    form.transient(root)
    form.grab_set()

    title_text = (
        "EDIT PATIENT" if is_editing
        else "NEW PATIENT"
    )

    ctk.CTkLabel(
        form,
        text=title_text,
        font=("Arial", 23, "bold"),
        text_color=TEXT
    ).pack(pady=(25, 20))
    
    old_patient = patients[index].copy() if is_editing else {}        # получение старых данных

    fields = [
        ("ФИО", "name"),
        ("Возраст", "age"),
        ("Рост (см)", "height"),
        ("Вес (кг)", "weight")
    ]

    entries = {}

    for label_text, field_name in fields:

        ctk.CTkLabel(
            form,
            text=label_text,
            font=("Arial", 13),
            text_color=TEXT
        ).pack(anchor="w", padx=45, pady=(8, 3))

        entry = ctk.CTkEntry(
            form,
            width=340,
            height=38,
            fg_color=PANEL,
            border_color=BORDER,
            text_color=TEXT
        )

        entry.pack(padx=40, pady=(0, 5))

        if field_name in old_patient:
            entry.insert(0, str(old_patient[field_name]))

        entries[field_name] = entry
        
    ctk.CTkLabel(
        form,
        text="Пол",
        font=("Arial", 13),
        text_color=TEXT
    ).pack(anchor="w", padx=45, pady=(10, 3))

    gender_menu = ctk.CTkOptionMenu(
        form,
        values=["Мужской", "Женский"],
        width=340,
        height=38,
        fg_color=BUTTON,
        button_color=ACCENT,
        button_hover_color=TEAL
    )

    gender_menu.pack(padx=40, pady=(0, 10))

    if is_editing:
        gender_menu.set(old_patient["gender"])
    else:
        gender_menu.set("Мужской")

    def save_form():
        """проверяет введённые данные и сохраняет пациента"""

        global patients, selected_index

        data = {
            "name": entries["name"].get(),
            "age": entries["age"].get(),
            "height": entries["height"].get(),
            "weight": entries["weight"].get(),
            "gender": gender_menu.get()
        }

        try:
            patient = validate_patient(data)

        except ValueError as error:
            messagebox.showwarning(
                "Проверьте данные",
                str(error),
                parent=form
            )
            return

        old_list = [p.copy() for p in patients]            # создание резервной копии

        if is_editing:
            patients[index] = patient
            selected_index = index
        else:
            patients.append(patient)
            selected_index = len(patients) - 1

        if not persist_patients():
            patients = old_list
            return

        render_table()
        form.destroy()

    save_button = ctk.CTkButton(
        form,
        text="Сохранить",
        command=save_form,
        width=340,
        height=42,
        fg_color=BUTTON,
        hover_color=ACCENT,
        font=("Arial", 14, "bold")
    )

    save_button.pack(pady=(20, 10))

    cancel_button = ctk.CTkButton(
        form,
        text="Отмена",
        command=form.destroy,
        width=340,
        height=38,
        fg_color="#A9BAC7",
        hover_color=SECONDARY
    )

    cancel_button.pack()


# удаление пациента
def delete_patient():
    """удаляет выбранную запись"""

    global patients, selected_index

    if selected_index is None:
        return

    answer = messagebox.askyesno(
        "Подтверждение",
        "Удалить выбранного пациента?",
        parent=root
    )

    if not answer:
        return

    old_list = [p.copy() for p in patients]

    patients.pop(selected_index)
    selected_index = None

    if not persist_patients():
        patients = old_list
        render_table()
        return

    render_table()


# статистика
def open_statistics():
    """Открывает окно сводной статистики."""

    show_statistics(root, patients.copy())


header = ctk.CTkFrame(
    root,
    fg_color="transparent"
)

header.pack(
    fill="x",
    padx=30,
    pady=(25, 10)
)

ctk.CTkLabel(
    header,
    text="MEDI DATA",
    font=("Arial", 30, "bold"),
    text_color=TEXT
).pack(anchor="w")

ctk.CTkLabel(
    header,
    text="PATIENT MANAGEMENT SYSTEM",
    font=("Arial", 12),
    text_color=SECONDARY
).pack(anchor="w", pady=(2, 0))


# счетчик пациентов
count_label = ctk.CTkLabel(
    root,
    text="Всего пациентов: 0",
    font=("Arial", 14, "bold"),
    text_color=TEXT
)

count_label.pack(anchor="w", padx=35, pady=(15, 10))


# панель кнопок
toolbar = ctk.CTkFrame(
    root,
    fg_color="transparent"
)

toolbar.pack(
    fill="x",
    padx=30,
    pady=10
)

add_button = ctk.CTkButton(
    toolbar,
    text="+ Добавить",
    command=lambda: open_patient_form(),
    fg_color=BUTTON,
    hover_color=ACCENT,
    height=38
)

add_button.pack(side="left", padx=5)

edit_button = ctk.CTkButton(
    toolbar,
    text="Редактировать",
    command=lambda: open_patient_form(selected_index),
    fg_color=TEAL,
    hover_color=ACCENT,
    height=38,
    state="disabled"
)

edit_button.pack(side="left", padx=5)

delete_button = ctk.CTkButton(
    toolbar,
    text="Удалить",
    command=delete_patient,
    fg_color="#C77C82",
    hover_color="#AD626A",
    height=38,
    state="disabled"
)

delete_button.pack(side="left", padx=5)

statistics_button = ctk.CTkButton(
    toolbar,
    text="Статистика",
    command=open_statistics,
    fg_color=BUTTON,
    hover_color=ACCENT,
    height=38
)

statistics_button.pack(side="right", padx=5)

refresh_button = ctk.CTkButton(
    toolbar,
    text="Обновить JSON",
    command=refresh_patients,
    fg_color="#8296A5",
    hover_color=SECONDARY,
    height=38
)

refresh_button.pack(side="right", padx=5)


# таблица
table_container = ctk.CTkFrame(
    root,
    fg_color=PANEL,
    corner_radius=12,
    border_width=1,
    border_color=BORDER
)

table_container.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=(10, 25)
)


table_header = ctk.CTkFrame(                # заголовки
    table_container,
    fg_color="#E8F2F8",
    corner_radius=8
)

table_header.pack(
    fill="x",
    padx=10,
    pady=(10, 5)
)

headers = [
    "ФИО",
    "Возраст",
    "Пол",
    "Рост",
    "Вес",
    "ИМТ"
]

for column, header_text in enumerate(headers):

    label = ctk.CTkLabel(
        table_header,
        text=header_text,
        font=("Arial", 13, "bold"),
        text_color=TEXT,
        anchor="w"
    )

    label.grid(
        row=0,
        column=column,
        sticky="ew",
        padx=8,
        pady=12
    )

    table_header.grid_columnconfigure(
        column,
        weight=1
    )


table = ctk.CTkScrollableFrame(             # строки таблицы
    table_container,
    fg_color=PANEL,
    corner_radius=8
)

table.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=(0, 10)
)


# запуск интерфейса
try:
    patients = load_patients(DATA_FILE)

except (OSError, ValueError, TypeError) as error:
    messagebox.showerror(
        "Ошибка загрузки",
        f"Не удалось загрузить данные:\n{error}",
        parent=root
    )
    patients = []

render_table()

root.mainloop()
