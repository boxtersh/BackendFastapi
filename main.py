from fastapi import FastAPI, status, HTTPException, Path, Query
from pydantic import BaseModel, Field
from typing import Optional, Annotated

from databases import TodosDBase


class TodoCreate(BaseModel):
    title: str = Field(
        min_length=6,
        max_length=100,
        description="Название задачи"
    )
    description: Optional[str] = Field(
        min_length=6,
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


class UpdateData(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=6,
        max_length=100,
        description="Описание поставленной задачи"
    )
    description: Optional[str] = Field(
        default=None,
        min_length=6,
        max_length=100,
        description="Описание поставленной задачи"
    )
    is_completed: bool = Field(
        default=None,
        description="Отметка о выполнении"
    )


class TodosListResponse(BaseModel):
    todos_list: list[TodoResponse] = []


app = FastAPI()
dbase = TodosDBase()


# Создать задачу
@app.post('/todos', response_model=TodoResponse, status_code=201)
async def add_todo(todo_data: TodoCreate) -> dict:
    id_ = dbase.increment_id
    todo_response = TodoResponse(
        id=id_,
        title=todo_data.title,
        description=todo_data.description,
        is_completed=todo_data.is_completed
    )
    dbase.todos_dict[id_] = todo_response
    return todo_response.model_dump()


# Получить все задачи
@app.get('/todos', response_model=TodosListResponse, status_code=200)
async def get_all_todo_taking_limit(limit: Annotated[Optional[int], Query()] = None) -> dict:
    list_todos = dbase.get_all_todo_taking_limit(limit)
    todos_list_response = TodosListResponse(todos_list=list_todos)
    return todos_list_response.model_dump()


# Получить задачу по id
@app.get('/todos/{id_}', response_model=TodoResponse, status_code=200)
async def get_todo_id(id_: Annotated[int, Path(..., gt=-1)]) -> dict:
    todo_response = dbase.get_todo_id(id_)
    if todo_response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Задача с указанным ID не найдена')
    return todo_response.model_dump()


# Изменить задачу целиком
@app.put('/todos/{id_}', response_model=TodoResponse, status_code=200)
async def put_todo_id(todo_data: TodoCreate, id_: Annotated[int, Path(..., gt=-1)]) -> dict:
    todo_response = dbase.get_todo_id(id_)
    if todo_response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Задача с указанным ID не найдена')
    todo_response.title = todo_data.title
    todo_response.description = todo_data.description
    todo_response.is_completed = todo_data.is_completed
    return todo_response.model_dump()


# Изменить указанные поля задачи
@app.patch('/todos/{id_}', response_model=TodoResponse, status_code=200)
async def patch_todo_id(id_: Annotated[int, Path(..., gt=-1)], update_date: UpdateData = None) -> dict:
    todo_response = dbase.selective_update_date(id_, update_date)
    if todo_response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Задача с указанным ID не найдена')
    return todo_response.model_dump()


# Удалить задачу по id
@app.delete('/todos/{id_}', response_model=TodoResponse, status_code=200)
async def delete_todo_id(id_: Annotated[int, Path(..., gt=-1)]) -> dict:
    todo_response = dbase.del_todo_id(id_)
    if todo_response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Задача с указанным ID не найдена')
    return todo_response.model_dump()