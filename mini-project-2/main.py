from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from database.connection import initialize_database
from routes.events import event_router
from routes.users import user_router


app = FastAPI()

# ROUTES
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")


# STARTUP EVENT
@app.on_event("startup")
async def start_database():
    await initialize_database()


# ROOT
@app.get("/")
async def home():
    return RedirectResponse(url="/event/")