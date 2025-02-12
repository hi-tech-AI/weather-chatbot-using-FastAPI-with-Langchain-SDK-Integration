from fastapi import FastAPI
from routers.chat import router as chat_router
from database.db_manager import init_db

app = FastAPI()

app.include_router(chat_router, prefix="/api")

if __name__ == "__main__":
    init_db()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
