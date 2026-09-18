#!/usr/bin/env bash
# Sauvegarde quotidienne de la base et des médias, conservée 35 jours.
# Planifiée par cron (voir le guide) :
#   0 3 * * * /opt/portfolio/deploy/ovh/sauvegarde.sh >> /var/log/portfolio-sauvegarde.log 2>&1
set -euo pipefail

cd "$(dirname "$0")"
set -a; . ./.env; set +a

DEST=/opt/portfolio-sauvegardes
JOUR=$(date +%F)
mkdir -p "$DEST"

docker compose exec -T db pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" --clean --if-exists \
  | gzip > "$DEST/base-$JOUR.sql.gz"

docker compose exec -T web tar -czf - -C /data media 2>/dev/null > "$DEST/medias-$JOUR.tar.gz" || true

find "$DEST" -type f -mtime +35 -delete
echo "$(date '+%F %T') sauvegarde OK : $(du -sh "$DEST" | cut -f1) au total"
