from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from api.routers import users, tasks


app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    title="Task manager API",
    description="API for managing tasks",
    version="0.2.0",
)

app.include_router(tasks.router)
app.include_router(users.router)


@app.get("/", description="Test endpoint for demonstration purposes")
def root():
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Hello World"})
