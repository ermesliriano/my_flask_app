# Flask DevOps App

Aplicación en **Flask** desplegada en **AWS** mediante pipeline CI/CD
con **Jenkins**, **Docker** y **Ansible**.\
Infraestructura definida como código con **Terraform**.

------------------------------------------------------------------------

## 1. Arquitectura

-   **App Flask** en contenedor Docker.
-   **Base de datos**: PostgreSQL (local) / SQLite persistente o RDS
    (producción).
-   **CI/CD**: Jenkins construye, testea, publica en Docker Hub y
    despliega con Ansible en EC2.
-   **Infraestructura**: EC2 para Jenkins (CI) y EC2 para la app,
    definidos con Terraform.
-   **Observabilidad**: endpoint `/health`, integración futura con
    CloudWatch.

------------------------------------------------------------------------

## 2. Entorno local

``` bash
git clone <URL_DEL_REPO>
cd <REPO>
docker-compose up --build
```

Acceso: - API: http://localhost:5000 - Healthcheck:
http://localhost:5000/health

------------------------------------------------------------------------

## 3. Tests y linting

``` bash
# Ejecutar pruebas unitarias
docker-compose run --rm web pytest

# Verificar estilo (PEP8)
docker-compose run --rm web flake8 .
```

Cobertura mínima requerida: **80%**.

------------------------------------------------------------------------

## 4. Pipeline CI/CD (Jenkins)

Stages principales: 1. Checkout código fuente 2. Tests (pytest) 3.
Linting (flake8) 4. Build imagen Docker 5. Push a Docker Hub 6. Deploy
en EC2 con Ansible

------------------------------------------------------------------------

## 5. Producción (AWS)

-   Despliegue en **EC2 t2.micro** (app).
-   Jenkins en **EC2 t2.medium**.
-   Seguridad mediante Security Groups (SSH restringido, 80/443
    abiertos).
-   Tráfico externo servido en puerto 80:

``` bash
curl http://<PUBLIC_IP>/health
# {"status": "ok"}
```

------------------------------------------------------------------------

## 6. Estructura del repositorio

    .
    ├── app/                 # Código Flask
    ├── infra/               # IaC con Terraform
    ├── deploy_app.yml       # Playbook Ansible
    ├── docker-compose.yml   # Dev local
    ├── Dockerfile           # Imagen app
    ├── Jenkinsfile          # Pipeline CI/CD
    ├── manage.py            # Init DB
    ├── run.py               # Entry point
    └── requirements.txt     # Dependencias

------------------------------------------------------------------------

## 7. Contribución

-   Modelo de ramas: feature → develop → main.
-   Revisiones por PR.
-   Requerido: tests + lint OK antes de merge.
