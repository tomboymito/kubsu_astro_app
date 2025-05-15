import sys
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .app.api.endpoints import router as api_router  # Измененный импорт
from .app.core.services.logger import setup_logger   # Измененный импорт

# Добавляем директорию проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(
    title="Astronomy Comet Analysis API",
    description="API for astronomical calculations related to comets",
    version="1.0.0",
)

# Инициализация логгера
setup_logger()

# Подключение роутера API
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return JSONResponse(
        content={"message": "Astronomy Comet Analysis API is running"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)