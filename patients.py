# расчёт ИМТ и работа с JSON
import json
import math
from pathlib import Path


ALLOWED_GENDERS = ["Мужской", "Женский"]


def calculate_bmi(height, weight):      # рассчитывает индекс массы тела, рост передаётся в сантиметрах, вес — в килограммах
    
    height = float(height)
    weight = float(weight)

    if not math.isfinite(height) or not math.isfinite(weight):
        raise ValueError("Рост и вес должны быть конечными числами")

    if height <= 0 or weight <= 0:
        raise ValueError("Рост и вес должны быть положительными")

    height_m = height / 100
    bmi = weight / (height_m ** 2)

    return round(bmi, 1)


def validate_patient(data):       # проверяет данные пациента и возвращает подготовленный словарь с рассчитанным ИМТ

    name = str(data.get("name", "")).strip()
    gender = str(data.get("gender", "")).strip()

    if not name:
        raise ValueError("Введите ФИО пациента")

    if gender not in ALLOWED_GENDERS:
        raise ValueError("Выберите пол из списка")

    try:
        age = int(data.get("age"))
        height = float(str(data.get("height")).replace(",", "."))
        weight = float(str(data.get("weight")).replace(",", "."))
    except (ValueError, TypeError):
        raise ValueError("Возраст, рост и вес должны быть числами")

    if age < 0 or age > 120:
        raise ValueError("Возраст должен быть от 0 до 120 лет")

    if not math.isfinite(height) or not math.isfinite(weight):
        raise ValueError("Рост и вес должны быть конечными числами")

    if height <= 0 or weight <= 0:
        raise ValueError("Рост и вес должны быть положительными")

    bmi = calculate_bmi(height, weight)

    return {
        "name": name,
        "age": age,
        "gender": gender,
        "height": round(height, 1),
        "weight": round(weight, 1),
        "bmi": bmi
    }


def save_patients(file_path, patients):        # сохраняет список пациентов в JSON; сначала записывает временный файл, затем заменяет им основной
    
    file_path = Path(file_path)
    temp_path = file_path.with_suffix(".tmp")

    with open(temp_path, "w", encoding="utf-8") as file:
        json.dump(
            patients,
            file,
            ensure_ascii=False,
            indent=4
        )

    temp_path.replace(file_path)


def load_patients(file_path):      # загружает пациентов из JSON, если файла ещё нет, возвращает пустой список

    file_path = Path(file_path)

    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("JSON должен содержать список пациентов")

    patients = []

    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Некорректная запись пациента")

        patient = validate_patient(item)
        patients.append(patient)

    return patients
