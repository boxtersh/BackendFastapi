from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from databases import TODOS
import validation as val

class TodoCreate(BaseModel):
    title: str = Field(
        min_length=6,
        max_length=100,
        description="Название задачи"
    )
    description: Optional[str] = Field(
        max_length=100,
        description="Описание поставленной задачи"
    )
    is_completed: bool = Field(
        default=False,
        description="Отметка о выполнении"
    )

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_completed: bool

app = FastAPI()
todos = TODOS()

# Создать задачу
@app.post('/todos', response_model=TodoResponse, status_code=201)
async def add_todo(todo_data: TodoCreate) -> dict:
    response_todo = todos.add_todo(todo_data)
    return response_todo

# Получить все задачи
@app.get('/todos')
async def get_todo_id() -> dict:
    if not val.list_is_empty(todos.todos_lst):
        print('Ошибка, Список задач пуст')
        return {'error': 'Список задач пуст'}
    response = dict()
    for obj in todos.todos_lst:
        response[obj.id] = todos.response_todo_json_sans_id(obj)
    return response

# Получить задачу по id
@app.get('/todos')
async def get_todo_id(id: int) -> dict:
    if not val.list_is_empty(todos.todos_lst):
        print('Ошибка, Список задач пуст')
        return {'error': 'Список задач пуст'}
    if not val.is_id(todos.todos_lst, id):
        print('Ошибка, id не найден')
        return {'error': 'Ошибка, id не найден'}
    return todos.get_todo_id(id)

# Изменить задачу целиком
@app.put('/todos')
async def get_todo_id(todo_data: TodoCreate, id: int) -> dict:
    if not val.list_is_empty(todos.todos_lst):
        print('Ошибка, Список задач пуст')
        return {'error': 'Список задач пуст'}
    if not val.is_id(todos.todos_lst, id):
        print('Ошибка, id не найден')
        return {'error': 'Ошибка, id не найден'}
    return todos.change_todo_attributes(todo_data, id)

'''
{
'title': 'Читать книги',
'description': 'Python, JS'
}
'''