# 1. Рядки (Strings):

def get_str_len(val: str):
    """Функція, яка приймає рядок і повертає його довжину."""
    return len(val)

my_str = "Hello world"
str_len = get_str_len(my_str)

print("\n--------------------------")
print("Напишіть функцію, яка приймає рядок і повертає його довжину.")
print(f"Довжина рядка '{my_str}' = {str_len} символів")


def join_strings(str1: str, str2: str):
    """Функція, яка приймає два рядки і повертає об'єднаний рядок."""
    return str1 + str2

str_1 = 'hi '
str_2 = 'there'
joined_strings = join_strings(str_1, str_2)

print("\n--------------------------")
print("Створіть функцію, яка приймає два рядки і повертає об'єднаний рядок.")
print(f"Рядок 1: {str_1}")
print(f"Рядок 2: {str_2}")
print(f"Обʼєднаний рядок: {joined_strings}")


# 2. Числа (Int/float):

def get_square(numb):
    """Функція, яка приймає число і повертає його квадрат."""
    return numb ** 2
number = 3
numb_square = get_square(number)

print("\n--------------------------")
print("Реалізуйте функцію, яка приймає число і повертає його квадрат.")
print(f"Квадрат від числа {number} = {numb_square}")


def add(numb1, numb2):
    return numb1 + numb2

def get_division_parts(numb1: int, numb2: int):
    int_part = numb1 // numb2
    remainder = numb1 % numb2

    return (int_part, remainder)

numerator = 12
denominator = 5
division_parts = get_division_parts(numerator, denominator)

numb1 = 123
numb2 = 321
add_result = add(numb1, numb2)

print("\n--------------------------")
print("Створіть функцію, яка приймає два числа і повертає їхню суму.")
print(f"{numb1} + {numb2} = {add_result}")

print("\n--------------------------")
print("Створіть функцію яка приймає 2 числа типу int, виконує операцію ділення та повертає чілу частину і залишок.")
print(f"{numerator}/{denominator}")
print(f"Ціла частина від ділення: {division_parts[0]}\nЗалишок: {division_parts[1]}")


# 3. Списки (Lists):

def get_average_value(numbs_list):
    elements_numb = len(numbs_list)
    elements_sum = sum(numbs_list)

    return elements_sum / elements_numb

numbs = [2.3, 12, 5.7, 4]
average_value = get_average_value(numbs)

print("\n--------------------------")
print("Напишіть функцію для обчислення середнього значення списку чисел.")
print(numbs)
print(f"Середнє значення списку: {average_value}")


def get_common_elements(list1, list2):
    result_list = []
    for item in list1:
        if any(type(item) == type(x) and item == x for x in list2)\
                and not any(type(item) == type(x) and item == x for x in result_list):
                result_list.append(item)

    return result_list

my_list_1 = [2, True, 1, 3, 2, 4, '7', (2, 1), False, 1]
my_list_2 = ['2', 2, 1, 5, True, 7, 0, False]
result_list = get_common_elements(my_list_1, my_list_2)

print("\n--------------------------")
print("Реалізуйте функцію, яка приймає два списки і повертає список, який містить спільні елементи обох списків.")
print(f"Список 1: {my_list_1}")
print(f"Список 2: {my_list_2}")
print(f"Спільні елементи: {result_list}")


# 4. Словники (Dictionaries):

def get_dict_keys(dictionary: dict):
    return list(dictionary.keys())

d = {"brand": "Apple", "model": "iPhone", "price": 40000}
dict_keys = get_dict_keys(d)

print("\n--------------------------")
print("Створіть функцію, яка приймає словник і виводить всі ключі цього словника.")
print(f"Словник: {d}")
print(f"Ключі цього словника: {dict_keys}")


def join_dicts(dict1: dict, dict2: dict):
    return dict1 | dict2

dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4, 'd': 5}
joined_dicts = join_dicts(dict1, dict2)

print("\n--------------------------")
print("Реалізуйте функцію, яка приймає два словники і повертає новий словник, який є об'єднанням обох словників.")
print(f"Словник1 : {dict1}")
print(f"Словник2 : {dict2}")
print(f"Новий словник: {joined_dicts}")


# 5. Множини (Sets):

def join_sets(set1: set, set2: set):
    return set1 | set2

set1 = {'a', 1, True}
set2 = {3.1, 'b', (1, 7), 1}
joined_sets = join_sets(set1, set2)

print("\n--------------------------")
print("Напишіть функцію, яка приймає дві множини і повертає їхнє об'єднання.")
print(f"Множина1 : {set1}")
print(f"Множина2 : {set2}")
print(f"Нова множина: {joined_sets}")


def is_subset(set_1: set, set_2: set):
    return 'Так' if set_1.issubset(set_2) else 'Ніт'

set_1 = {1, 'a'}
set_2 = {1, 3, 5, 'a'}
result = is_subset(set_1, set_2)

print("\n--------------------------")
print("Створіть функцію, яка перевіряє, чи є одна множина підмножиною іншої.")
print(f"Множина1 : {set_1}")
print(f"Множина2 : {set_2}")
print(f"Чи є множина {set_1} підмножиною {set_2}: {result}")


# 6. Умовні вирази та цикли:

def is_number_even_or_odd(numb: int):
    return 'Парне' if not numb % 2 else 'Непарне'

result1 = is_number_even_or_odd(7)
result2 = is_number_even_or_odd(8)

print("\n--------------------------")
print("Реалізуйте функцію, яка приймає число і виводить 'Парне', якщо число парне, і 'Непарне', якщо непарне.")
print(f"Число 7: {result1}")
print(f"Число 8: {result2}")


def get_even_numbs(numbs):
    return list(filter(lambda x: x % 2 == 0, numbs))

numbs_list = [1, 3, 56, 34, 4.6, -24]
even_numbs = get_even_numbs(numbs_list)

print("\n--------------------------")
print("Створіть функцію, яка приймає список чисел і повертає новий список, що містить тільки парні числа.")
print(f"Вихідний список: {numbs_list}")
print(f"Список з парними числами: {even_numbs}")


# 7. Написати лямбда-функцію визначальну парне/непарне.

even_or_odd = lambda numb: 'Парне' if not numb % 2 else 'Непарне'

print("\n--------------------------")
print("Функція приймає параметр (число) і якщо парне, видає слово “парне”, якщо ні - то “не парне”.")
print(f"Число 7: {even_or_odd(7)}")

