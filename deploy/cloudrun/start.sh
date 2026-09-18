#!/usr/bin/env bash
# Démarrage d'une instance Cloud Run : Gunicorn uniquement.
set -euo pipefail

if [ -z "${EMAIL_HOST_USER:-}" ] || [ -z "${EMAIL_HOST_PASSWORD:-}" ]; then
  echo "⚠ ALERTE : EMAIL_HOST_USER / EMAIL_HOST_PASSWORD absents."
  echo "  Les codes de validation 2FA ne partiront pas. Vérifier Secret Manager."
fi

if [ -z "${GS_BUCKET_NAME:-}" ]; then
  echo "⚠ ALERTE : GS_BUCKET_NAME absent — les médias iraient sur le disque"
  echo "  éphémère de l'instance et disparaîtraient à son arrêt."
fi

# Une instance Cloud Run traite les requêtes en parallèle via les threads ;
# timeout 0 : c'est Cloud Run qui borne la durée des requêtes.
exec gunicorn config.wsgi:application \
  --bind=0.0.0.0:"${PORT:-8080}" \
  --workers 1 \
  --threads 8 \
  --timeout 0 \
  --access-logfile '-' \
  --error-logfile '-'
