# Proyecto IRCA - Monorepo

Este repositorio contiene dos aplicaciones del sistema IRCA:

1. Backend en FastAPI para logica de negocio, API y persistencia.
2. Frontend en Angular para visualizacion, gestion y consumo de la API.

## Estructura General

```text
.
|-- back/
|-- front/
|-- build.sh
`-- README.md
```

## Proyecto Backend (FastAPI)

Servicio API responsable de autenticacion, entidades del dominio IRCA, estadisticas y prediccion.

### Arbol de directorios del backend

```text
back/
|-- alembic/
|   `-- versions/
|-- app/
|   |-- core/
|   |-- llms/
|   |   `-- notebooks/
|   |       |-- experimentos/
|   |       `-- exploracion/
|   |-- models/
|   |-- routers/
|   |-- schemas/
|   `-- services/
`-- tests/
```
Descripcion de directorios backend:

- back/alembic/: configuracion y scripts de migraciones de base de datos.
- back/alembic/versions/: historial de migraciones versionadas.
- back/app/: codigo principal de la API FastAPI.
- back/app/core/: configuracion central, seguridad y utilidades transversales.
- back/app/llms/: artefactos y recursos de modelos de prediccion.
- back/app/llms/notebooks/: notebooks para exploracion y experimentacion.
- back/app/models/: modelos ORM de las entidades de dominio.
- back/app/routers/: endpoints HTTP agrupados por modulo funcional.
- back/app/schemas/: esquemas de validacion y serializacion de datos.
- back/app/services/: logica de negocio desacoplada de los routers.
- back/tests/: pruebas automatizadas del backend.

## Proyecto Frontend (Angular)

Aplicacion web para consumir la API de IRCA, mostrar dashboard, vistas de datos, formularios, tablas y graficos.

### Arbol de directorios del frontend

```text
front/
`-- src/
  |-- app/
  |   |-- components/
  |   |-- icons/
  |   |-- interceptors/
  |   |-- layout/
  |   |   `-- default-layout/
  |   |-- models/
  |   |-- services/
  |   `-- views/
  |       |-- base/
  |       |-- buttons/
  |       |-- charts/
  |       |-- dashboard/
  |       |-- forms/
  |       `-- icons/
  |-- assets/
  |   |-- brand/
  |   `-- images/
  |       `-- avatars/
  |-- components/
  |   |-- docs-callout/
  |   |-- docs-example/
  |   `-- docs-link/
  |-- environments/
  `-- scss/
```
Descripcion de directorios frontend:

- front/src/: codigo fuente principal de la aplicacion Angular.
- front/src/app/: modulos de aplicacion, vistas, componentes y servicios.
- front/src/app/components/: componentes reutilizables del dominio de la app.
- front/src/app/icons/: iconografia y recursos visuales de UI.
- front/src/app/interceptors/: interceptores HTTP para errores y limites.
- front/src/app/layout/: estructura visual general de la aplicacion.
- front/src/app/layout/default-layout/: plantilla base usada por las vistas.
- front/src/app/models/: interfaces y modelos de datos del frontend.
- front/src/app/services/: consumo de API y servicios de estado/utilidad.
- front/src/app/views/: paginas o pantallas principales.
- front/src/assets/: recursos estaticos como imagenes y marca.
- front/src/components/: componentes compartidos y utilitarios del template.
- front/src/environments/: variables de entorno por ambiente.
- front/src/scss/: estilos globales, tema y ajustes visuales.

## Despliegue en Cloud Run
# prueba

El despliegue se plantea con dos servicios independientes en Cloud Run:

1. Servicio backend: API FastAPI.
2. Servicio frontend: aplicacion Angular.

### Prerrequisitos

```bash
gcloud auth login
gcloud config set project PROJECT_ID
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
```

### 1) Despliegue del backend en Cloud Run

El backend ya incluye Dockerfile en back/, por lo que se puede construir y desplegar como contenedor.

```bash
# Desde la raiz del repo
gcloud builds submit back \
  --tag REGION-docker.pkg.dev/PROJECT_ID/REPO/irca-back:latest

gcloud run deploy irca-back \
  --image REGION-docker.pkg.dev/PROJECT_ID/REPO/irca-back:latest \
  --platform managed \
  --region REGION \
  --allow-unauthenticated
```

Variables recomendadas para backend en Cloud Run:

- DATABASE_URL
- SECRET_KEY
- ALGORITHM
- ACCESS_TOKEN_EXPIRE_MINUTES

### 2) Despliegue del frontend en Cloud Run

Para frontend se recomienda compilar Angular y servir archivos estaticos con Nginx en un contenedor dedicado.

```bash
# Desde la raiz del repo
gcloud builds submit front \
  --tag REGION-docker.pkg.dev/PROJECT_ID/REPO/irca-front:latest

gcloud run deploy irca-front \
  --image REGION-docker.pkg.dev/PROJECT_ID/REPO/irca-front:latest \
  --platform managed \
  --region REGION \
  --allow-unauthenticated
```

Configuracion recomendada para frontend:

- Ajustar environment.production.ts con la URL publica del servicio backend.
- Definir CORS en backend para permitir origen del frontend desplegado.

## Nota de arquitectura

Al tener servicios separados en Cloud Run, frontend y backend pueden escalar y versionarse de forma independiente.
