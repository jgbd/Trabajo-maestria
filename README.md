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

El despliegue recomendado para este repositorio es en un solo servicio Cloud Run
usando el Dockerfile de la raiz (imagen fullstack: FastAPI + Angular).

### Prerrequisitos

```bash
gcloud auth login
gcloud config set project PROJECT_ID
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
```

### 1) Construir y publicar imagen fullstack

```bash
# Desde la raiz del repo
gcloud builds submit . \
  --tag REGION-docker.pkg.dev/PROJECT_ID/REPO/ircaback:latest
```

### 2) Desplegar servicio Cloud Run

```bash
gcloud run deploy ircaback \
  --image REGION-docker.pkg.dev/PROJECT_ID/REPO/ircaback:latest \
  --platform managed \
  --region REGION \
  --allow-unauthenticated \
  --port 8080
```

### 3) Variables de entorno sugeridas

Para despliegue sin base externa (arranque inmediato):

```bash
--set-env-vars USE_SQLITE=true,PORT=8080
```

Para MySQL en produccion:

```bash
--set-env-vars USE_SQLITE=false,DB_USER=...,DB_PASSWORD=...,DB_HOST=...,DB_PORT=3306,DB_NAME=...,PORT=8080
```

### 4) Ver logs de una revision fallida

```bash
gcloud run revisions logs read REVISION_NAME \
  --service ircaback \
  --region REGION \
  --limit 200
```

Si una revision vuelve a fallar por puerto, casi siempre el error real aparece en
estos logs (excepcion en import, variables faltantes o comando de inicio).
