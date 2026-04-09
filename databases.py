import copy

class TODOS:
    def __init__(self):
        self.__id = -1
        self.todos_lst = []

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
        response_todo = copy.deepcopy(todo)
        setattr(response_todo, 'id', self.__id)
        self.todos_lst.append(response_todo)
        return self.response_todo_json(response_todo)

    def get_todo_id(self, id: int) -> dict:
        for obj in self.todos_lst:
            if obj.id == id:
                return self.response_todo_json(obj)

    def change_todo_attributes(self, todo_data, id):
        for obj in self.todos_lst:
            if obj.id == id:
                obj.title = todo_data.todo_data
                obj.description = todo_data.description
                obj.is_completed = todo_data.is_completed
                return self.response_todo_json_sans_id(obj)