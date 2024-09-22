#!/bin/bash
STORE_DIR=/volume1/mnt/rebs
DATE=$(date +"%Y-%m-%d")
SQL_FILE=db-rebs-${DATE}.sql

cp "${STORE_DIR}"/prod/volume/backups/"${SQL_FILE}" "${STORE_DIR}"/dev/volume/sql/
