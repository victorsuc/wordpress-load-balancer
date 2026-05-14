#!/usr/bin/env sh
set -eu

CONTAINERS="${1:-}"

if [ "$CONTAINERS" != "1" ] && [ "$CONTAINERS" != "2" ] && [ "$CONTAINERS" != "3" ]; then
  echo "Uso: ./scripts/use-nginx-upstream.sh <1|2|3>"
  exit 1
fi

CONFIG_SOURCE="nginx-${CONTAINERS}wp.conf"

if [ ! -f "$CONFIG_SOURCE" ]; then
  echo "Arquivo $CONFIG_SOURCE nao encontrado."
  exit 1
fi

cp "$CONFIG_SOURCE" nginx.conf
docker compose exec nginx nginx -t
docker compose exec nginx nginx -s reload

echo "Nginx configurado para usar ${CONTAINERS} container(s) WordPress."
