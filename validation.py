# Задача с id есть в списке задач
def todos_is_in_todos_dict(todos_dict: dict, id_: int) -> "TodoResponse | bool":
    todo_response = todos_dict.get(id_, False)
    return todo_response

# Список пуст
def todos_dict_is_empty(todos_dict: dict) -> bool:
    return len(todos_dict) == 0

# В БД элементов >= limit
def todos_is_greater_or_equal_limit(todos_dict: dict, limit: int) -> bool:
    return len(todos_dict) >= limit

# Получили пустой запрос
def update_data_is_nane(update_date):
    return update_date is None


