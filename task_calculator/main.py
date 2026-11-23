import customtkinter as ctk
from calculations import calculate_expression

# НАСТРОЙКИ ОКНА
ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.title("calculator by cybernytik")
root.geometry("420x680")
root.minsize(380, 620)
root.configure(fg_color="#190F15")

# ЦВЕТОВАЯ ПАЛИТРА
BG = "#190F15"
PANEL = "#2B1721"
BUTTON = "#38232D"
BUTTON_HOVER = "#57303F"
OPERATOR = "#913B55"
OPERATOR_HOVER = "#B34C6B"
ACCENT = "#D65B7B"
TEXT = "#F8E8ED"
SECONDARY = "#B99AA5"

# СОЗДАНИЕ СПИСКА ДЛЯ ИСТОРИИ ВЫЧИСЛЕНИЙ
history = []

# ЗАГОЛОВОК
title = ctk.CTkLabel(
    root,
    text="CALCULATOR",
    font=("Verdana", 22, "bold"),
    text_color=TEXT
)
title.pack(pady=(15, 8))

# ПАНЕЛЬ ВВОДА
display_frame = ctk.CTkFrame(
    root,
    fg_color=PANEL,
    corner_radius=20
)
display_frame.pack(fill="x", padx=20, pady=5)

def validate_input(new_value):
    allowed = "0123456789+-*/(). "

    if len(new_value) > 100:
        return False

    # Разрешаем буквы только для sqrt
    cleaned = new_value.replace("sqrt", "")

    return all(char in allowed for char in cleaned)

entry = ctk.CTkEntry(
    display_frame,
    font=("Verdana", 25),
    justify="right",
    height=65,
    fg_color=PANEL,
    text_color=TEXT,
    border_width=0,
    corner_radius=15,
    placeholder_text="Введите выражение...",
    validate="key",
    validatecommand=(root.register(validate_input), "%P")
)
entry.pack(fill="x", padx=12, pady=(12, 4))

message = ctk.CTkLabel(
    display_frame,
    text="",
    font=("Verdana", 12),
    text_color=ACCENT
)
message.pack(anchor="e", padx=15, pady=(0, 10))

# ФУНКЦИИ
def add_to_entry(value):
    entry.insert("insert", value)

def square():
    add_to_entry("**2")

def clear():
    entry.delete(0, "end")
    message.configure(text="")

def backspace():
    position = entry.index("insert")
    if position > 0:
        entry.delete(position - 1, position)

def update_history():
    history_label.configure(
        text="\n".join(history)
    )


def calculate():
    expression = entry.get()

    try:
        result = calculate_expression(expression)

        history.append(f"{expression} = {result}")

        # Оставляем только три последних вычисления
        if len(history) > 3:
            history.pop(0)

        update_history()

        entry.delete(0, "end")
        entry.insert(0, str(result))

        message.configure(
            text="Результат вычислен",
            text_color=SECONDARY
        )

    except ZeroDivisionError:
        message.configure(
            text="Деление на ноль!",
            text_color=ACCENT
        )

    except (ValueError, SyntaxError, TypeError, OverflowError):
        message.configure(
            text="Некорректное выражение",
            text_color=ACCENT
        )


# КНОПКИ
buttons = [
    ("AC", 0, 0), ("(", 1, 0), (")", 2, 0), ("x²", 3, 0),
    ("7", 0, 1), ("8", 1, 1), ("9", 2, 1), ("÷", 3, 1),
    ("4", 0, 2), ("5", 1, 2), ("6", 2, 2), ("×", 3, 2),
    ("1", 0, 3), ("2", 1, 3), ("3", 2, 3), ("−", 3, 3),
    ("√", 0, 4), ("0", 1, 4), (".", 2, 4), ("+", 3, 4)
]

# СОЗДАНИЕ КНОПОК
button_frame = ctk.CTkFrame(
    root,
    fg_color=BG
)
button_frame.pack(fill="both", expand=True, padx=20, pady=8)

for i in range(4):
    button_frame.grid_columnconfigure(i, weight=1)

for i in range(6):
    button_frame.grid_rowconfigure(i, weight=1)


for text, column, row in buttons:

    if text == "AC":
        command = clear
        color = OPERATOR



    elif text == "√":
        command = lambda: add_to_entry("sqrt(")
        color = OPERATOR

    elif text == "x²":
        command = square
        color = OPERATOR

    else:
        symbols = {"÷": "/", "×": "*", "−": "-"}
        value = symbols.get(text, text)
        command = lambda v=value: add_to_entry(v)

        color = OPERATOR if text in ("+", "÷", "×", "−") else BUTTON

    hover = OPERATOR_HOVER if color == OPERATOR else BUTTON_HOVER


    button = ctk.CTkButton(
        button_frame,
        text=text,
        font=("Verdana", 18, "bold"),
        fg_color=color,
        hover_color=hover,
        text_color=TEXT,
        corner_radius=16,
        height=55,
        command=command
    )

    button.grid(
        row=row,
        column=column,
        padx=5,
        pady=5,
        sticky="nsew"
    )

# КНОПКА УДАЛЕНИЯ ОДНОГО СИМВОЛА
delete_button = ctk.CTkButton(
    button_frame,
    text="⌫",
    font=("Verdana", 20, "bold"),
    fg_color=OPERATOR,
    hover_color=OPERATOR_HOVER,
    text_color=TEXT,
    corner_radius=16,
    command=backspace
)

delete_button.grid(
    row=5,
    column=0,
    columnspan=2,
    padx=5,
    pady=5,
    sticky="nsew"
)


# КНОПКА РАВНО
equal_button = ctk.CTkButton(
    button_frame,
    text="=",
    font=("Verdana", 20, "bold"),
    fg_color=ACCENT,
    hover_color=OPERATOR_HOVER,
    text_color=TEXT,
    corner_radius=16,
    command=calculate
)
    
equal_button.grid(
    row=5,
    column=2,
    columnspan=2,
    padx=5,
    pady=5,
    sticky="nsew"
)

# ВЫЧИСЛЕНИЕ ПО ENTER
root.bind("<Return>", lambda event: calculate())

# ОЧИСТКА ПО ESCAPE
root.bind("<Escape>", lambda event: clear())

# ПАНЕЛЬ ИСТОРИИ
history_frame = ctk.CTkFrame(
    root,
    fg_color=PANEL,
    corner_radius=15
)

history_frame.pack(
    fill="x",
    padx=20,
    pady=(0, 10)
)

history_title = ctk.CTkLabel(
    history_frame,
    text="RECENT HISTORY",
    font=("Verdana", 12, "bold"),
    text_color=SECONDARY
)

history_title.pack(anchor="w", padx=15, pady=(7, 3))

history_label = ctk.CTkLabel(
    history_frame,
    text="История пока пуста",
    font=("Verdana", 12),
    text_color=TEXT,
    justify="left"
)

history_label.pack(anchor="w", padx=15, pady=(0, 7))

# ЗАПУСК
root.mainloop()
