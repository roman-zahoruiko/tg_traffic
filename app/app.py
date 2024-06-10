from fastapi import FastAPI
from auth.router import auth_router, admin_router
from message.router import message_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(message_router)
