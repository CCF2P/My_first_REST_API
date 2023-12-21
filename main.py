from fastapi import FastAPI
import uvicorn

from routers.MainRouter import router
from routers.AuthRouter import auth_router


app = FastAPI()

app.include_router(router)
app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port="8000")
