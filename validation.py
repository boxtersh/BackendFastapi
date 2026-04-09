# Есть задача с id в списке?
def is_id(lst: dict, id: int) -> bool:
    return lst.get(id, False)

# Список пуст
def list_is_empty(lst: list) -> bool:
    return len(lst) == 0

