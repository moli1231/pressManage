#!/usr/bin/env bash
set -euo pipefail

DB_FILE=${1:-pressure_gauges.db}
BACKUP_DIR=${2:-./backups}
TS=$(date +"%Y%m%d_%H%M%S")
mkdir -p "$BACKUP_DIR"
cp "$DB_FILE" "$BACKUP_DIR/pressure_gauges_$TS.db"
echo "backup created: $BACKUP_DIR/pressure_gauges_$TS.db"
