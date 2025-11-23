from app.database import Base, engine
from app.models import user, departamento, municipio, vereda, prestadorServicio, sistemaDistribucion, puntoMuestreo, resultado 
from app.routers import users
import app.services
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter
import uvicorn

from app.routers import estadisticas, municipios
# Crear las tablas en la base de datos al iniciar el programa
Base.metadata.create_all(bind=engine)

# Inicialización del servidor FastAPI
app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Error de validación",
            "details": [
                {"field": err["loc"][-1], "message": err["msg"]}
                for err in exc.errors()
            ]
        },
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las direcciones
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los encabezados
)


api_router = APIRouter(prefix="/api")

# Registrar las rutas
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(estadisticas.router, prefix="/estadisticas", tags=["estadisticas"])
api_router.include_router(municipios.router, prefix="/municipios", tags=["municipios"])

app.include_router(api_router)

@app.get("/")
async def read_root():
    return {"message": "¡Bienvenido a mi FastAPI!"}

def start():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    print("Servidor FastAPI iniciado en http://localhost:8000")
