import customtkinter as ctk
from matplotlib.figure import Figure        # создает область расположения графиков
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg        # встраивает графики MatPlotLib в tkinter


BG = "#F2F8FC"
PANEL = "#FFFFFF"
ACCENT = "#6BAED6"
TEAL = "#75C6C0"
TEXT = "#243746"
SECONDARY = "#8296A5"
BORDER = "#DCEAF2"


def show_statistics(parent, patients):

    window = ctk.CTkToplevel(parent)
    window.title("MEDI DATA — Analytics")
    window.geometry("1100x800")
    window.minsize(850, 650)
    window.configure(fg_color=BG)

    title = ctk.CTkLabel(
        window,
        text="PATIENT ANALYTICS",
        font=("Arial", 26, "bold"),
        text_color=TEXT
    )
    title.pack(pady=(20, 10))

    if not patients:
        ctk.CTkLabel(
            window,
            text="Недостаточно данных для анализа",
            font=("Arial", 16),
            text_color=SECONDARY
        ).pack(pady=40)

        return

    # подготовка данных

    ages = [p["age"] for p in patients]
    bmis = [p["bmi"] for p in patients]
    genders = [p["gender"] for p in patients]

    male_bmi = [
        p["bmi"] for p in patients
        if p["gender"] == "Мужской"
    ]

    female_bmi = [
        p["bmi"] for p in patients
        if p["gender"] == "Женский"
    ]

    # создание области для графиков

    figure = Figure(figsize=(10, 7), dpi=100)
    figure.patch.set_facecolor(PANEL)

    ax1 = figure.add_subplot(221)        # графики в сетке 2x2
    ax2 = figure.add_subplot(222)
    ax3 = figure.add_subplot(223)
    ax4 = figure.add_subplot(224)

    # 1. распределение по полу

    gender_counts = [
        genders.count("Мужской"),
        genders.count("Женский")
    ]

    ax1.pie(
        gender_counts,
        labels=["Мужской", "Женский"],
        autopct="%1.1f%%",
        colors=[ACCENT, TEAL],
        startangle=90
    )

    ax1.set_title("Распределение по полу")

    # 2. распределение по возрасту

    ax2.hist(
        ages,
        bins="auto",
        color=ACCENT,
        edgecolor="white"
    )

    ax2.set_title("Распределение возраста")
    ax2.set_xlabel("Возраст")
    ax2.set_ylabel("Количество пациентов")

    # 3. распределение ИМТ с учётом пола

    min_bmi = min(bmis) - 0.5
    max_bmi = max(bmis) + 0.5

    if male_bmi:
        ax3.hist(
            male_bmi,
            bins=8,
            range=(min_bmi, max_bmi),
            alpha=0.65,
            color=ACCENT,
            label="Мужской"
        )

    if female_bmi:
        ax3.hist(
            female_bmi,
            bins=8,
            range=(min_bmi, max_bmi),
            alpha=0.65,
            color=TEAL,
            label="Женский"
        )

    ax3.set_title("Распределение ИМТ по полу")
    ax3.set_xlabel("ИМТ")
    ax3.set_ylabel("Количество")
    ax3.legend()

    # 4. зависимость ИМТ от возраста

    ax4.scatter(
        ages,
        bmis,
        color=ACCENT,
        alpha=0.8
    )

    ax4.set_title("ИМТ и возраст")
    ax4.set_xlabel("Возраст")
    ax4.set_ylabel("ИМТ")

    # оформление графиков

    axes = [ax1, ax2, ax3, ax4]

    for ax in axes:
        ax.set_facecolor(PANEL)

        ax.title.set_color(TEXT)
        ax.xaxis.label.set_color(SECONDARY)
        ax.yaxis.label.set_color(SECONDARY)

        ax.tick_params(colors=SECONDARY)

        for spine in ax.spines.values():
            spine.set_color(BORDER)

    figure.tight_layout(pad=3)

    # встраиваем графики в окно CustomTkinter

    canvas = FigureCanvasTkAgg(
        figure,
        master=window
    )

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    # сохраняем ссылки на объекты, пока открыто окно статистики

    window.figure = figure
    window.canvas = canvas
