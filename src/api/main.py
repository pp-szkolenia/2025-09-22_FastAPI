from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from api.routers import users, tasks


app = FastAPI()

app.include_router(tasks.router)
app.include_router(users.router)


@app.get("/")
def root():
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Hello World"})
