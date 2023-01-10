from app.db.models_creator import create_tables, fulfill_tables
from app.db.utils import check_db_status
from app.api.controllers import controller_exec_search
from app.api.models import Job, SearchForm
from http import HTTPStatus
from typing import List
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
jobs = {}

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def init_db():
    error = create_tables()
    if error:
        raise Exception(error)


@app.post("/search")
async def search(forms: list[SearchForm]):
    return controller_exec_search([form.dict() for form in forms])


@app.get("/check_db")
async def check_db():
    status = dict()
    status['message'] = check_db_status()
    return status


def process_fulfillment(task_id):
    error = fulfill_tables()
    jobs[task_id].status = "completed" if not error else "error"
    jobs[task_id].message = error


@app.get('/fulfill_tables', response_model=Job, status_code=HTTPStatus.ACCEPTED)
async def make_tables_fulfillment(background_tasks: BackgroundTasks):
    new_task = Job()
    jobs[new_task.uid] = new_task
    background_tasks.add_task(process_fulfillment, new_task.uid)
    return new_task


@app.get("/fulfill_tables/status")
async def status_handler():
    return jobs
