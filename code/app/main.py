from typing import Union
from app.db.models_creator import create_tables, fulfill_tables
from app.db.db_utils import check_db_status
from app.api.models import Job
from http import HTTPStatus
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()
jobs = {}


@app.on_event("startup")
async def init_db():
    error = create_tables()
    if error:
        raise Exception(error)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/check_db")
async def check_db():
    status = dict()
    status['message'] = check_db_status()
    return status

def process_fulfillment(task_id):
    error = fulfill_tables()
    jobs[task_id].status = "completed"
    jobs[task_id].message = error


@app.get('/fulfill_tables', status_code=HTTPStatus.ACCEPTED)
async def work(background_tasks: BackgroundTasks):
    new_task = Job()
    jobs[new_task.uid] = new_task
    background_tasks.add_task(process_fulfillment, new_task.uid)
    return new_task


@app.get("/fulfill_tables/status")
async def status_handler():
    return jobs

# async def async_fulfill_tables(job_key):
#     jobs = context['jobs']
#     error = await fulfill_tables()
#     status = dict()
#     status['status'] = "ok"
#     if error:
#         status['status'] = "not ok"
#         status['message'] = error
#     jobs[job_key] = status

# @app.get("/fulfill_tables")
# async def init_tables():
#     identifier = str(uuid.uuid4())
#     context['jobs'][identifier] = {}
#     asyncio.run_coroutine_threadsafe(async_fulfill_tables(identifier), loop=asyncio.get_running_loop())

#     return {"identifier": identifier}

#     error = fulfill_tables()
#     status = dict()
#     status['status'] = "ok"
#     if error:
#         status['status'] = "not ok"
#         status['message'] = error
#     return status

# @app.get("/fulfill_tables/status")
# async def init_tables_status():
#     return {
#         'all': list(context['jobs'].values()),
#     }
