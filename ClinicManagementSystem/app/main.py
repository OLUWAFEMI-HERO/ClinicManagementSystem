from fastapi import FastAPI
from .database import init_db
from .routes import users

app = FastAPI(title="Healthcare Payment & Appointment API")

init_db()

# register routers
app.include_router(users.router, tags=["users"])

@app.get("/")
def root():
    return {"msg": "Healthcare API running"}
