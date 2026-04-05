#!/bin/bash
DATE=$(date +%Y-%m-%d)
BACKUP_DIR=/mnt/hdd/backups/vaultwarden
mkdir -p $BACKUP_DIR
cp -r /opt/docker/vaultwarden $BACKUP_DIR/vaultwarden-$DATE
# Mantener solo los últimos 4 backups
ls -t $BACKUP_DIR | tail -n +5 | xargs -I {} rm -rf $BACKUP_DIR/{}
echo "Backup completado: vaultwarden-$DATE"
