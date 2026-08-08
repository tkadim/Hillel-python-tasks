import time
from fastapi import FastAPI
from starlette.requests import Request
from routers import router as main_router


app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
  # 1. Дії ПЕРЕД тим, як запит потрапить в ендпоінт
  start_time = time.time()

  # call_next передає запит далі по ланцюжку до потрібного ендпоінту
  response = await call_next(request)

  # 2. Дії ПІСЛЯ того, як ендпоінт сформував відповідь
  process_time = time.time() - start_time

  # Додаємо кастомний заголовок із часом виконання запиту
  response.headers["x-process-time"] = str(process_time)

  return response


app.include_router(main_router)
