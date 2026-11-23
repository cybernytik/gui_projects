import customtkinter as ctk

from matplotlib.figure import Figure                                  # создает область расположения графиков
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg       # встраивает графики MatPlotLib в TKinter


def show_statistics(parent, patients):
    # Создаём окно аналитики
    window = ctk.CTkToplevel(parent)
    window.title("MEDI DATA — Analytics")
    window.geometry("1100x800")
    window.configure(fg_color="#F2F8FC")
    window.transient(parent)

    title = ctk.CTkLabel(
        window,
        text="PATIENT ANALYTICS",
        font=("Arial", 26, "bold"),
        text_color="#243746"
    )
    title.pack(pady=15)

    if not patients:
        ctk.CTkLabel(
            window,
            text="Недостаточно данных для построения графиков",
            font=("Arial", 16),
            text_color="#8296A5"
        ).pack(pady=30)
        return

    # Извлекаем данные
    ages = [int(p["age"]) for p in patients]
    bmis = [float(p["bmi"]) for p in patients]
    genders = [p["gender"] for p in patients]

    male_bmi = [
        float(p["bmi"])
        for p in patients
        if p["gender"] == "Мужской"
    ]

    female_bmi = [
        float(p["bmi"])
        for p in patients
        if p["gender"] == "Женский"
    ]

    # Создаём область с четырьмя графиками
    figure = Figure(figsize=(10, 7), dpi=100)
    figure.patch.set_facecolor("#FFFFFF")

    ax1 = figure.add_subplot(221)      # графики в сетке 2*2
    ax2 = figure.add_subplot(222)
    ax3 = figure.add_subplot(223)
    ax4 = figure.add_subplot(224)

    # График 1. Распределение по полу
    gender_counts = [
        genders.count("Мужской"),
        genders.count("Женский")
    ]

    if sum(gender_counts) > 0:
        ax1.pie(
            gender_counts,
            labels=["Мужской", "Женский"],
            autopct="%1.1f%%",
            colors=["#6BAED6", "#75C6C0"],
            startangle=90
        )

    ax1.set_title("Распределение по полу")

    # График 2. Распределение по возрасту
    ax2.hist(
        ages,
        bins="auto",
        color="#6BAED6",
        edgecolor="white"
    )
    ax2.set_title("Распределение возраста")
    ax2.set_xlabel("Возраст")
    ax2.set_ylabel("Количество пациентов")

    # График 3. Распределение ИМТ по полу
    if male_bmi:
        ax3.hist(
            male_bmi,
            bins=10,
            alpha=0.6,
            color="#6BAED6",
            label="Мужской"
        )

    if female_bmi:
        ax3.hist(
            female_bmi,
            bins=10,
            alpha=0.6,
            color="#75C6C0",
            label="Женский"
        )

    ax3.set_title("Распределение ИМТ по полу")
    ax3.set_xlabel("ИМТ")
    ax3.set_ylabel("Количество")
    ax3.legend()

    # График 4. Зависимость ИМТ от возраста
    ax4.scatter(
        ages,
        bmis,
        color="#6BAED6",
        alpha=0.8
    )
    ax4.set_title("ИМТ и возраст")
    ax4.set_xlabel("Возраст")
    ax4.set_ylabel("ИМТ")

    # Общие настройки
    figure.tight_layout(pad=3)

    canvas = FigureCanvasTkAgg(
        figure,
        master=window
    )
    canvas.draw()
    canvas.get_tk_widget().pack(
        fill="both",
        expand=True,
        padx=15,
        pady=15
    )

