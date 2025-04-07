from fastapi import FastAPI
from routes import router as restaurant_router
from menu_routes import router as menu_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI is running!"}

# Include routers
app.include_router(restaurant_router)
app.include_router(menu_router)
