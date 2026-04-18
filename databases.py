class Todos:
    def __init__(self):
        self.__id = -1
        self.todos_dict = {}

    @property
    def increment_id (self):
        self.__id += 1
        return self.__id

    def get_all_todo_taking_limit(self, limit: int|None) -> list:
        if len(self.todos_dict) == 0:
            return []
        list_todos = [todo_response for todo_response in self.todos_dict.values()]
        if limit is None:
            return list_todos
        elif len(self.todos_dict) >= limit:
            return list_todos[:limit]
        return list_todos

    def get_todo_id(self, id_: int) -> "TodoResponse | bool":
        if self.todos_dict.get(id_, False):
            return self.todos_dict[id_]
        return False

    def selective_update_date(self, id_: int, update_date: 'UpdateData') -> 'TodoResponse | bool':
        todo_id = self.get_todo_id(id_)
        if not todo_id:
            return False
        if update_date is None:
            return todo_id
        for key, item in vars(update_date).items():
            if not item is None:
                setattr(todo_id, key, item)
        return todo_id

    def full_update_date_todo_attributes(self, todo_data, id_):
        self.todos_dict[id_] = todo_data
        return {id_: todo_data}

    def del_todo_id(self, id_: int):
        if self.get_todo_id(id_):
            buff_todo_response = self.get_todo_id(id_)
            del self.todos_dict[id_]
            return buff_todo_response
        return False