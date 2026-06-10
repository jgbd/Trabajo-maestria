from app.database import Base, engine
from app.models import user, departamento, municipio, vereda, prestadorServicio, sistemaDistribucion, puntoMuestreo, resultado 
# from app.routers import users  # Commented out - user management removed from public API
import app.services
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uvicorn

# NEW IMPORTS for Phase 1
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.rate_limiter import limiter, rate_limit_exceeded_handler
from app.core.config import settings

from app.routers import estadisticas, municipios, prediccion

# Crear las tablas en la base de datos al iniciar el programa
Base.metadata.create_all(bind=engine)

# Inicialización del servidor FastAPI con configuración
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add rate limiter to app state
app.state.limiter = limiter

# Register rate limit error handler
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

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

# CORS Configuration for public API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # ["*"] for public data access
    allow_credentials=False,  # No credentials needed for public data
    allow_methods=settings.ALLOWED_METHODS,  # ["GET", "OPTIONS"] - read-only
    allow_headers=settings.ALLOWED_HEADERS,  # ["Content-Type"]
)


api_router = APIRouter(prefix="/api")

# Registrar las rutas
# User management removed from public API - for internal admin use only
# api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(estadisticas.router, prefix="/estadisticas", tags=["estadisticas"])
api_router.include_router(municipios.router, prefix="/municipios", tags=["municipios"])
api_router.include_router(prediccion.router, tags=["prediccion"])

app.include_router(api_router)

# ============================================================================
# Serve Static Files (Angular Frontend)
# ============================================================================
# Mount static files for Angular app
# Priority: 1. /api/* (API routes), 2. /assets/* (static assets), 3. /* (SPA)

@app.get("/api")
async def api_root():
    """API root endpoint - shows available endpoints"""
    return {
        "message": "¡Bienvenido a IRCA Water Quality API!", 
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "estadisticas": "/api/estadisticas",
            "municipios": "/api/municipios",
            "prediccion": "/api/prediccion"
        }
    }

# Fallback root endpoint (if static files not mounted)
@app.get("/health")
async def health_check():
    """Health check endpoint for Docker/Cloud Run"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }


# Serve Angular build when available.
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
INDEX_FILE = STATIC_DIR / "index.html"

if (STATIC_DIR / "assets").exists():
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")


@app.get("/", include_in_schema=False)
async def serve_root():
    if INDEX_FILE.exists():
        return FileResponse(INDEX_FILE)
    raise HTTPException(status_code=404, detail="Frontend no disponible")


@app.get("/{full_path:path}", include_in_schema=False)
async def spa_fallback(full_path: str):
    # Avoid intercepting API and docs paths handled by FastAPI routes.
    reserved_prefixes = ("api", "docs", "redoc", "openapi.json", "health")
    if full_path.startswith(reserved_prefixes):
        raise HTTPException(status_code=404, detail="Ruta no encontrada")

    requested_file = STATIC_DIR / full_path
    if requested_file.is_file():
        return FileResponse(requested_file)

    if INDEX_FILE.exists():
        return FileResponse(INDEX_FILE)

    raise HTTPException(status_code=404, detail="Frontend no disponible")

def start():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    print(f"Servidor {settings.PROJECT_NAME} iniciado en http://localhost:8000")
