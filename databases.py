import copy

class TODOS:
    def __init__(self):
        self.__id = -1
        self.todos_lst = {}

    @staticmethod
    def response_todo_json(todo) -> dict:
        return {'id': todo.id,
                'title': todo.title,
                'description': todo.description,
                'is_completed': todo.is_completed}

    @staticmethod
    def response_todo_json_sans_id(todo) -> dict:
        return {'title': todo.title,
                'description': todo.description,
                'is_completed': todo.is_completed}

    def add_todo(self, todo) -> dict:
        self.__id += 1
        self.todos_lst[self.__id] = todo
        return {self.__id: todo}

    def get_todo_id(self, id: int) -> dict:
        for obj in self.todos_lst:
            if obj.id == id:
                return self.response_todo_json(obj)

    def full_change_todo_attributes(self, todo_data, id):
        self.todos_lst[id] = todo_data
        return {id: todo_data}