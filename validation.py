# Есть задача с id в списке?
def is_id(lst: list, id: int) -> bool:
    for obj in lst:
        return obj.id == id

# Список не пустой!
def list_is_empty(lst: list) -> bool:
    return len(lst) > 0

