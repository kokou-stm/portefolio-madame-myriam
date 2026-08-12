# Image de production — Portfolio Myriam Dossou d'Almeida
FROM python:3.12-slim

# Sorties Python non tamponnées (logs visibles en temps réel), pas de .pyc.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Dépendances d'abord : couche mise en cache tant que requirements.txt ne change pas.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Code de l'application.
COPY . .

# Fichiers statiques figés à la construction (WhiteNoise + manifeste compressé).
# Une clé factice suffit : collectstatic ne lit aucun secret.
RUN DJANGO_SECRET_KEY=build-only DJANGO_DEBUG=0 \
    python manage.py collectstatic --noinput

EXPOSE 8000

# migrate + amorçage + Gunicorn (voir startup.sh).
CMD ["./startup.sh"]
