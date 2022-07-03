from fastapi import FastAPI
from .account.router import account_router


app = FastAPI()
app.include_router(account_router, prefix="/user")
