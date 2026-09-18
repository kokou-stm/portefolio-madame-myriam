#!/usr/bin/env bash
# Import de l'export de la base Azure dans la base PostgreSQL Render.
# À lancer une fois, depuis la racine du dépôt, après la création du Blueprint :
#   bash deploy/render/importer-donnees.sh <chemin/vers/complet.json>
#
# L'adresse demandée est l'« External Database URL » de portfolio-db
# (Render → portfolio-db → Connect → External).
set -euo pipefail

EXPORT="${1:?Chemin de complet.json attendu en argument}"
[ -f "$EXPORT" ] || { echo "✗ Fichier introuvable : $EXPORT"; exit 1; }

read -r -s -p "External Database URL de portfolio-db (Render) : " RENDER_URL; echo

# Garde-fous : jamais la base Azure, toujours une base Render.
case "$RENDER_URL" in
  *azure*) echo "✗ Adresse Azure refusée : ce script écrase la base cible."; exit 1 ;;
  *render.com*) ;;
  *) echo "✗ L'adresse ne ressemble pas à une base Render (…render.com)."; exit 1 ;;
esac

export DATABASE_URL="$RENDER_URL"
PY=.venv/bin/python

echo "→ Schéma"
$PY manage.py migrate --noinput

# La base Render ne contient à ce stade que l'amorçage automatique du premier
# démarrage : on la vide pour ne garder que les données réelles.
echo "→ Remplacement de l'amorçage par les données exportées"
$PY manage.py flush --noinput
$PY manage.py loaddata "$EXPORT"

echo "→ Contrôle"
$PY -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.apps import apps
from django.contrib.auth.models import User
for nom in ['Article', 'Video', 'Realisation', 'Photo', 'Message', 'EmailAutorise']:
    print(f'  {nom:14}', apps.get_model('cv', nom).objects.count())
print(f'  {\"Comptes\":14}', User.objects.count())
"
echo "✓ Import terminé."
