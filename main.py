import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox            # диалоговое окно подтверждения

# Настройки внешнего вида
ctk.set_appearance_mode("light")

root = ctk.CTk()
root.title("MEDI DATA — Patient Management")
root.geometry("1000x700")
root.minsize(850, 600)
root.configure(fg_color="#F2F8FC")

# Цветовая палитра
BG = "#F2F8FC"
PANEL = "#FFFFFF"
ACCENT = "#6BAED6"
TEAL = "#75C6C0"
BUTTON = "#4E91BD"
TEXT = "#243746"
SECONDARY = "#8296A5"
BORDER = "#DCEAF2"

# Заголовок приложения
header = ctk.CTkFrame(root, fg_color="transparent")
header.pack(fill="x", padx=30, pady=(25, 15))

title = ctk.CTkLabel(
    header,
    text="MEDI DATA",
    font=("Arial", 28, "bold"),
    text_color=TEXT
)
title.pack(anchor="w")

subtitle = ctk.CTkLabel(
    header,
    text="Patient management system",
    font=("Arial", 13),
    text_color=SECONDARY
)
subtitle.pack(anchor="w")

# Карточка со статистикой
stats_card = ctk.CTkFrame(
    root,
    fg_color=PANEL,
    corner_radius=18,
    border_width=1,
    border_color=BORDER
)
stats_card.pack(fill="x", padx=30, pady=10)

patients_count_title = ctk.CTkLabel(
    stats_card,
    text="Всего пациентов",
    font=("Arial", 14),
    text_color=SECONDARY
)
patients_count_title.pack(anchor="w", padx=20, pady=(15, 0))

patients_count = ctk.CTkLabel(
    stats_card,
    text="0",
    font=("Arial", 30, "bold"),
    text_color=ACCENT
)
patients_count.pack(anchor="w", padx=20, pady=(0, 15))

# Область таблицы
table_frame = ctk.CTkFrame(
    root,
    fg_color=PANEL,
    corner_radius=18,
    border_width=1,
    border_color=BORDER
)
table_frame.pack(fill="both", expand=True, padx=30, pady=15)

table_title = ctk.CTkLabel(
    table_frame,
    text="Список пациентов",
    font=("Arial", 18, "bold"),
    text_color=TEXT
)
table_title.pack(anchor="w", padx=20, pady=20)

# Названия колонок
columns = ("name", "age", "gender", "height", "weight", "bmi")

# Создание таблицы
table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

table.heading("name", text="ФИО")
table.heading("age", text="Возраст")
table.heading("gender", text="Пол")
table.heading("height", text="Рост")
table.heading("weight", text="Вес")
table.heading("bmi", text="ИМТ")

# Ширина колонок
table.column("name", width=240, anchor="w")
table.column("age", width=90, anchor="center")
table.column("gender", width=100, anchor="center")
table.column("height", width=100, anchor="center")
table.column("weight", width=100, anchor="center")
table.column("bmi", width=100, anchor="center")

# Окно добавления пациента
def add_patient():
    form = ctk.CTkToplevel(root)
    form.title("Добавление пациента")
    form.geometry("400x500")
    form.resizable(False, False)
    form.configure(fg_color=BG)
    form.transient(root)
    form.grab_set()

    form_title = ctk.CTkLabel(
        form,
        text="Новый пациент",
        font=("Arial", 22, "bold"),
        text_color=TEXT
    )
    form_title.pack(pady=(25, 20))

    # Поля формы
    name_entry = ctk.CTkEntry(form, placeholder_text="ФИО")
    name_entry.pack(fill="x", padx=30, pady=8)

    age_entry = ctk.CTkEntry(form, placeholder_text="Возраст")
    age_entry.pack(fill="x", padx=30, pady=8)

    gender_box = ctk.CTkComboBox(
        form,
        values=["Мужской", "Женский"]
    )
    gender_box.pack(fill="x", padx=30, pady=8)
    gender_box.set("Мужской")

    height_entry = ctk.CTkEntry(form, placeholder_text="Рост (см)")
    height_entry.pack(fill="x", padx=30, pady=8)

    weight_entry = ctk.CTkEntry(form, placeholder_text="Вес (кг)")
    weight_entry.pack(fill="x", padx=30, pady=8)

    message = ctk.CTkLabel(
        form,
        text="",
        text_color="#D65B5B"
    )
    message.pack(pady=5)

    def save_patient():
        name = name_entry.get().strip()
        age = age_entry.get().strip()
        gender = gender_box.get()
        height = height_entry.get().strip()
        weight = weight_entry.get().strip()

        if not name or not age or not height or not weight:
            message.configure(text="Заполните все поля")
            return

        try:
            age = int(age)
            height = float(height.replace(",", "."))
            weight = float(weight.replace(",", "."))

            if age <= 0 or height <= 0 or weight <= 0:
                raise ValueError

            bmi = weight / (height / 100) ** 2            # расчет ИМТ

        except ValueError:
            message.configure(text="Проверьте введённые данные")
            return

        table.insert(
            "",
            "end",
            values=(
                name,
                age,
                gender,
                height,
                weight,
                round(bmi, 1)
            )
        )

        # Обновляем количество пациентов
        count = len(table.get_children())
        patients_count.configure(text=str(count))

        form.destroy()

    save_button = ctk.CTkButton(
        form,
        text="Сохранить пациента",
        fg_color=BUTTON,
        hover_color=ACCENT,
        text_color="white",
        corner_radius=12,
        command=save_patient
    )
    save_button.pack(fill="x", padx=30, pady=15)


# Редактирование пациента
def edit_patient():
    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Внимание",
            "Сначала выберите пациента"
        )
        return

    item = selected[0]
    values = table.item(item, "values")

    form = ctk.CTkToplevel(root)
    form.title("Редактирование пациента")
    form.geometry("400x500")
    form.resizable(False, False)
    form.configure(fg_color=BG)
    form.transient(root)
    form.grab_set()

    title = ctk.CTkLabel(
        form,
        text="Редактирование данных",
        font=("Arial", 22, "bold"),
        text_color=TEXT
    )
    title.pack(pady=(25, 20))

    name_entry = ctk.CTkEntry(form, placeholder_text="ФИО")
    name_entry.pack(fill="x", padx=30, pady=8)
    name_entry.insert(0, values[0])

    age_entry = ctk.CTkEntry(form, placeholder_text="Возраст")
    age_entry.pack(fill="x", padx=30, pady=8)
    age_entry.insert(0, values[1])

    gender_box = ctk.CTkComboBox(
        form,
        values=["Мужской", "Женский"]
    )
    gender_box.pack(fill="x", padx=30, pady=8)
    gender_box.set(values[2])

    height_entry = ctk.CTkEntry(form, placeholder_text="Рост (см)")
    height_entry.pack(fill="x", padx=30, pady=8)
    height_entry.insert(0, values[3])

    weight_entry = ctk.CTkEntry(form, placeholder_text="Вес (кг)")
    weight_entry.pack(fill="x", padx=30, pady=8)
    weight_entry.insert(0, values[4])

    message = ctk.CTkLabel(form, text="", text_color="#D65B5B")
    message.pack(pady=5)

    def save_changes():
        name = name_entry.get().strip()
        age = age_entry.get().strip()
        gender = gender_box.get()
        height = height_entry.get().strip()
        weight = weight_entry.get().strip()

        if not name or not age or not height or not weight:
            message.configure(text="Заполните все поля")
            return

        try:
            age = int(age)
            height = float(height.replace(",", "."))
            weight = float(weight.replace(",", "."))

            if age <= 0 or height <= 0 or weight <= 0:
                raise ValueError

            bmi = weight / (height / 100) ** 2

        except ValueError:
            message.configure(text="Проверьте введённые данные")
            return

        table.item(
            item,
            values=(
                name,
                age,
                gender,
                height,
                weight,
                round(bmi, 1)
            )
        )

        form.destroy()

    save_button = ctk.CTkButton(
        form,
        text="Сохранить изменения",
        fg_color=BUTTON,
        hover_color=ACCENT,
        command=save_changes
    )
    save_button.pack(fill="x", padx=30, pady=15)


# Удаление пациента
def delete_patient():
    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Внимание",
            "Сначала выберите пациента"
        )
        return

    answer = messagebox.askyesno(            # функция для создания диалогового окна с вопросом yes/no (в случае yes -> возвращение булевой True, в случае no -> возвращение булевой False, чем отличается от askquestion, где возвращаются 'yes' и 'no')
        "Подтверждение",
        "Удалить выбранного пациента?"
    )

    if answer:
        for item in selected:
            table.delete(item)

        patients_count.configure(
            text=str(len(table.get_children()))
        )


# Кнопка добавления
add_button = ctk.CTkButton(
    table_frame,
    text="+ Добавить пациента",
    fg_color=BUTTON,
    hover_color=ACCENT,
    text_color="white",
    corner_radius=12,
    command=add_patient
)
add_button.pack(anchor="e", padx=15, pady=(0, 12))

# Кнопка изменения
edit_button = ctk.CTkButton(
    table_frame,
    text="Редактировать",
    fg_color=TEAL,
    hover_color=ACCENT,
    text_color=TEXT,
    corner_radius=12,
    command=edit_patient
)
edit_button.pack(anchor="e", padx=15, pady=(0, 8))

# Кнопка удаления
delete_button = ctk.CTkButton(
    table_frame,
    text="Удалить",
    fg_color="#D98282",
    hover_color="#C76565",
    text_color="white",
    corner_radius=12,
    command=delete_patient
)
delete_button.pack(anchor="e", padx=15, pady=(0, 12))

# Размещение таблицы
table.pack(fill="both", expand=True, padx=15, pady=(0, 15))


root.mainloop()
