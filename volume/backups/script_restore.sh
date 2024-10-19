#!/bin/bash
DATE=$(date +"%Y-%m-%d")
SQL_FILE=/var/backups/backup-${DATE}.sql

mariadb -u"${USER}" -p"${PASSWORD}" "${DATABASE}" < "${SQL_FILE}"
