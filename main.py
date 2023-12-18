from fastapi import FastAPI

from routers.MainRouter import router
from routers.AuthRouter import auth_router


app = FastAPI()

app.include_router(router)
app.include_router(auth_router)
