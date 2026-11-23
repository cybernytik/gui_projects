import customtkinter as ctk

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

root.mainloop()

