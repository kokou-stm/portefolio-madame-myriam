#!/usr/bin/env bash
# Job Cloud Run `portfolio-migrate` : exécuté une fois par déploiement, avant
# la mise à jour du service. Mêmes étapes que startup.sh côté Azure.
set -euo pipefail

echo "→ Migrations"
python manage.py migrate --noinput

echo "→ Amorçage (sans effet si le contenu existe déjà)"
python manage.py initialiser

echo "→ Retrait des articles de démonstration"
python manage.py purger_demo --rubriques
