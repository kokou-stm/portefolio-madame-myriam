# Image Google Cloud Run — Portfolio Myriam Dossou d'Almeida
# Construite depuis la racine du dépôt :
#   docker build -f deploy/cloudrun/Dockerfile .
# Indépendante de l'image Azure (Dockerfile racine), qui reste inchangée.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Dépendances communes, puis celles propres à Cloud Run (stockage des médias).
COPY requirements.txt .
COPY deploy/cloudrun/requirements.txt requirements-cloudrun.txt
RUN pip install -r requirements.txt -r requirements-cloudrun.txt

COPY . .

RUN DJANGO_SECRET_KEY=build-only DJANGO_DEBUG=0 \
    python manage.py collectstatic --noinput

# Cloud Run fournit le port dans $PORT (8080 par défaut).
EXPOSE 8080

# Le service ne fait que servir : migrations et amorçage passent par le job
# Cloud Run `portfolio-migrate` (deploy/cloudrun/migrate.sh), exécuté une fois
# par déploiement plutôt qu'à chaque démarrage d'instance.
CMD ["deploy/cloudrun/start.sh"]
