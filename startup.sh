#!/usr/bin/env bash
# Commande de démarrage Azure App Service.
set -euo pipefail

# Seul /home survit aux redémarrages et aux redéploiements sur App Service.
mkdir -p "${DJANGO_DATA_DIR:-.}/media"

# Un secret SMTP absent casserait l'envoi des codes 2FA sans autre signe qu'un
# échec de connexion à l'administration : on le signale au démarrage.
if [ -z "${EMAIL_HOST_USER:-}" ] || [ -z "${EMAIL_HOST_PASSWORD:-}" ]; then
  echo "⚠ ALERTE : EMAIL_HOST_USER / EMAIL_HOST_PASSWORD absents."
  echo "  Les codes de validation 2FA ne partiront pas. Vérifier les secrets GitHub."
else
  echo "✓ Identifiants SMTP présents (expéditeur : ${EMAIL_HOST_USER})"
fi

echo "→ Migrations"
python manage.py migrate --noinput

echo "→ Amorçage (sans effet si le contenu existe déjà)"
python manage.py initialiser

echo "→ Purge des articles de démonstration"
python manage.py purger_demo --rubriques

echo "→ Démarrage de Gunicorn"
# Port pilotable : 80 sur Container Instances (URL sans port), 8000 par défaut.
exec gunicorn config.wsgi:application \
  --bind=0.0.0.0:"${PORT:-8000}" \
  --workers 2 \
  --threads 4 \
  --timeout 120 \
  --access-logfile '-' \
  --error-logfile '-'
