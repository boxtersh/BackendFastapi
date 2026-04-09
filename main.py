from fastapi import FastAPI, status, HTTPException, Path
from pydantic import BaseModel, Field
from typing import Optional, Annotated

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
async def get_todo_id(limit: int=None) -> dict:
    if val.dict_ge_limit(todos.todos_lst, limit):
        if limit is None:
            return todos.todos_lst
        return dict(list(todos.todos_lst.items())[:limit])
    return todos.todos_lst

# Получить задачу по id
@app.get('/todos/{id}')
async def get_todo_id(id: int) -> dict:
    if not val.id_in_todos(todos.todos_lst, id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail='Задача с указанным ID не найдена')
    return todos.get_todo_id(id)

# Изменить задачу целиком
@app.put('/todos/{id}')
async def put_todo_id(todo_data: TodoCreate, id: int) -> dict:
    if not val.id_in_todos(todos.todos_lst, id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return todos.full_change_todo_attributes(todo_data, id)

# Изменить указанные поля задачи
@app.patch('/todos')
async def patch_todo_id(todo_data_select: dict, id: int) -> dict:
    ...

# Удалить задачу по id
@app.delete('/todos/{id}')
async def delete_todo_id(id: int) -> dict:
    if not val.id_in_todos(todos.todos_lst, id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return todos.del_todo_id(id)



a = {'title': 'Читать книги',
'description': 'Python, JS',
'is_completed': False
}
