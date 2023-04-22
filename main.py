from fastapi import FastAPI
from routes.trade import trade
app =FastAPI()

app.include_router(trade)