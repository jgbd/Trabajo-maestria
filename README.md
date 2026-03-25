# Proyecto IRCA - Monorepo

Monorepo que contiene tanto el backend como el frontend para el sistema de gestión y análisis de datos de calidad de agua IRCA.

## 📋 Estructura del Proyecto

```
.
├── back/              # Backend (Python/FastAPI)
│   ├── app/          # Aplicación principal
│   ├── tests/        # Tests unitarios
│   ├── alembic/      # Migraciones de base de datos
│   ├── pyproject.toml # Configuración y dependencias
│   └── alembic.ini   # Configuración de Alembic
│
├── front/            # Frontend (Angular)
│   ├── src/          # Código fuente
│   ├── package.json  # Dependencias npm
│   └── angular.json  # Configuración de Angular
│
└── README.md         # Este archivo
```

## 🚀 Backend (Python/FastAPI)

### Descripción
API REST construida con **FastAPI** para gestionar:
- Usuarios y autenticación
- Departamentos, municipios y veredas
- Puntos de muestreo
- Resultados de análisis de calidad de agua
- Estadísticas y reportes
- Modelos de clasificación e predicción IRCA

### Tecnologías
- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para base de datos
- **Alembic**: Migraciones de base de datos
- **Machine Learning**: Modelos IRCA integrados

### Estructura
- `/app/main.py` - Punto de entrada de la aplicación
- `/app/database.py` - Configuración de la base de datos
- `/app/models/` - Modelos de datos (SQLAlchemy)
- `/app/schemas/` - Esquemas de validación (Pydantic)
- `/app/routers/` - Rutas/endpoints de la API
- `/app/services/` - Lógica de negocio
- `/app/llms/` - Modelos de Machine Learning (Jupyter Notebooks)

### Requisitos
- Python 3.10+
- PostgreSQL o SQLite
- pip o conda

### Instalación y ejecución

```bash
# Navegar a la carpeta del backend
cd back/

# Crear ambiente virtual
python -m venv venv

# Activar el ambiente virtual
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate  # En Windows

# Instalar dependencias
pip install -e .

# Configurar variables de entorno
cp .env.example .env  # Si existe

# Ejecutar migraciones de base de datos
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`
Documentación interactiva (Swagger): `http://localhost:8000/docs`

### Testing
```bash
pytest tests/
```

---

## 🎨 Frontend (Angular)

### Descripción
Interfaz web moderna construida con **Angular** que proporciona:
- Dashboard de estadísticas
- Gestión de datos de puntos de muestreo
- Visualización de resultados de análisis
- Gráficos y reportes
- Mapas interactivos
- Autenticación de usuarios

### Tecnologías
- **Angular 17+**: Framework frontend
- **TypeScript**: Lenguaje de programación
- **SCSS**: Estilos avanzados
- **Components**: Componentes reutilizables
- **Services**: Servicios para consumir API
- **Routing**: Navegación entre vistas

### Estructura
- `/src/app/` - Componentes y lógica de la aplicación
- `/src/app/views/` - Páginas principales
- `/src/app/components/` - Componentes reutilizables
- `/src/app/services/` - Servicios (consumo de API)
- `/src/assets/` - Imágenes, fonts, etc.
- `/src/scss/` - Estilos globales y temas

### Requisitos
- Node.js 18+ y npm
- Angular CLI (opcional pero recomendado)

### Instalación y ejecución

```bash
# Navegar a la carpeta del frontend
cd front/

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm start
# o
ng serve
```

La aplicación estará disponible en `http://localhost:4200`

### Build para producción
```bash
npm run build
# o
ng build --configuration production
```

### Testing
```bash
npm test
# o
ng test
```

---

## 🔄 Flujo de Desarrollo

### Configuración inicial completa

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd proyectos

# 2. Configurar Backend
cd back/
python -m venv venv
source venv/bin/activate
pip install -e .
alembic upgrade head
# Configurar variables de entorno en .env

# 3. En otra terminal, configurar Frontend
cd front/
npm install

# 4. En una terminal, ejecutar Backend
cd back/
source venv/bin/activate
uvicorn app.main:app --reload

# 5. En otra terminal, ejecutar Frontend
cd front/
npm start
```

## 📝 Variables de Entorno

### Backend (`back/.env`)
```
DATABASE_URL=postgresql://user:password@localhost/irca_db
# o para SQLite:
DATABASE_URL=sqlite:///./irca.db

SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (`front/environment.ts`)
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'
};
```

## 🗄️ Base de Datos

Modelos principales:
- **User**: Usuarios del sistema
- **Departamento**: Divisiones administrativas
- **Municipio**: Municipios dentro de departamentos
- **Vereda**: Veredas dentro de municipios
- **PuntoMuestreo**: Puntos de recolección de datos
- **Resultado**: Resultados de análisis de calidad de agua
- **SistemaDistribucion**: Sistemas de distribución de agua
- **PrestadorServicio**: Entidades prestadoras de servicios

Las migraciones se encuentran en `/back/alembic/versions/`

## 🔐 Autenticación

El sistema utiliza JWT (JSON Web Tokens) para autenticación:
1. El usuario se autentica en el frontend
2. El backend retorna un token acceso
3. El frontend incluye el token en las solicitudes subsecuentes
4. El backend valida el token y retorna los recursos

## 📊 Modelos de Machine Learning

En `/back/app/llms/` se encuentran los modelos IRCA:
- `model_irca_clasification.ipynb` - Clasificación de calidad de agua
- `model_irca_precition.ipynb` - Predicción de índices IRCA
- `model_irca.py` - Implementación de modelos en producción
- `model_irca_experimentos.ipynb` - Experimentación con modelos

## 🐛 Troubleshooting

### Backend no conecta a la base de datos
- Verificar que PostgreSQL/SQLite esté corriendo
- Revisar la conexión en las variables de entorno
- Ejecutar migraciones: `alembic upgrade head`

### Frontend no conecta con API
- Verificar que el backend esté ejecutándose en `http://localhost:8000`
- Revisar la URL de API en `src/environments/environment.ts`
- Revisar la consola del navegador para errores CORS

### Problemas con dependencias Python
- Eliminar y recrear el virtual environment
- Ejecutar: `pip install --upgrade pip setuptools wheel`
- Reinstalar: `pip install -e .`

## 📚 Documentación Adicional

- **API Docs**: `http://localhost:8000/docs` (Swagger UI)
- **ReDoc**: `http://localhost:8000/redoc` (Documentación alternativa)
- **Angular Docs**: https://angular.io/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com/

## 📧 Contacto y Soporte

Para reportar problemas o sugerencias, contactar al equipo de desarrollo.

---

**Última actualización**: Marzo 2026
