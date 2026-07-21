fibonacci_list = []

def get_fibonacci_list(left_value: int, right_value: int, steps_number: int):

    fibonacci_list.append(left_value)

    if steps_number == 1:
        return left_value

    else:
        return get_fibonacci_list(right_value, left_value + right_value, steps_number - 1)


rabbits_number = get_fibonacci_list(2, 2, 10)

print(fibonacci_list)

print(f"Кількість кролеків на 10 місяць: {rabbits_number}")
