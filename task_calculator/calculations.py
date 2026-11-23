import ast    # abstract syntax tree, позволяет разобрать выражение на синтаксические элементы
import math
import operator    # предоставляет функции математических операций


OPERATIONS = {                       # словарь разрешенных операций
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow
}


def evaluate(node):      # рекурсивная функция для вычисления математических операций
    # числа
    if isinstance(node, ast.Constant):      # проверка на числовой тип через константу
        if type(node.value) in (int, float):
            return node.value

    # арифметические операции
    if isinstance(node, ast.BinOp):      # бинарная операция с двумя операндами
        if type(node.op) not in OPERATIONS:      # сама операция
            raise ValueError("Недопустимая операция")

        left = evaluate(node.left)       # левый операнд
        right = evaluate(node.right)    # правый операнд

        if isinstance(node.op, ast.Pow):
            if abs(right) > 100:
                raise ValueError("Слишком большая степень")

        result = OPERATIONS[type(node.op)](left, right)    # определение типа -> поиск в словаре допустимых операций -> передача операндов -> сохранение в result

        if type(result) not in (int, float):
            raise ValueError("Недопустимый результат")

        if abs(result) > 1e100:
            raise ValueError("Слишком большое число")

        return result

    # унарный плюс и минус
    if isinstance(node, ast.UnaryOp):      # унарные - с одним операндом
        if isinstance(node.op, ast.UAdd):
            return evaluate(node.operand)

        if isinstance(node.op, ast.USub):
            return -evaluate(node.operand)

    # Квадратный корень
    if isinstance(node, ast.Call):
        if (
            isinstance(node.func, ast.Name)    # проверка вызванной функции
            and node.func.id == "sqrt"
            and len(node.args) == 1        # проверка, передан ли только 1 аргумент
            and not node.keywords          # проверка на наличие именованных аргументов
        ):
            number = evaluate(node.args[0])

            if number < 0:
                raise ValueError("Корень из отрицательного числа")

            return math.sqrt(number)

    raise ValueError("Недопустимое выражение")


def calculate_expression(expression):
    if not expression.strip():
        raise ValueError("Введите выражение")

    if len(expression) > 100:
        raise ValueError("Максимум 100 символов")

    tree = ast.parse(expression, mode="eval")      # строка -> синтаксическое дерево; разбор только одного выражения, а не целой программы

    return evaluate(tree.body)        # передача корневого узла в рекурсивную функцию и возврат результатов вычисления
