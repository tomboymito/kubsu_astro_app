import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from backend.app.api.endpoints import router as api_router
from backend.app.core.services.logger import setup_logger
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="Astronomy Comet Analysis API",
    description="API for astronomical calculations related to comets",
    version="1.0.0",
)

# Настройка логирования
setup_logger()

# Подключение Prometheus метрик
Instrumentator().instrument(app).expose(app)

# Подключение роутера API
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return JSONResponse(
        content={"message": "Astronomy Comet Analysis API is running"}
    )

@app.get("/health")
async def health_check():
    return {
        "status": "OK",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)