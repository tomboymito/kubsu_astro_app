from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api.endpoints import router as api_router
from app.core.services.logger import setup_logging


app = FastAPI(
    title="Astronomy Comet Analysis API",
    description="API for astronomical calculations related to comets",
    version="1.0.0",
)


# Настройка логирования
setup_logging()


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
