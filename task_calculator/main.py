import customtkinter as ctk
from calculations import calculate_expression

def calculate():                    # функция вычисления
    expression = entry.get()

    try:
        result = calculate_expression(expression)

        entry.delete(0, "end")
        entry.insert(0, str(result))

    except ZeroDivisionError:
        entry.delete(0, "end")
        entry.insert(0, "Деление на 0!")

    except (ValueError, SyntaxError, TypeError, OverflowError):
        entry.delete(0, "end")
        entry.insert(0, "Ошибка")
