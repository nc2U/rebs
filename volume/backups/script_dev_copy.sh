#!/bin/bash
DATE=$(date +"%Y-%m-%d")
SQL_FILE=db-rebs-${DATE}.sql

cp /mnt/nfs/prod/volume/backups/"${SQL_FILE}" /mnt/nfs/dev/volume/sql/
