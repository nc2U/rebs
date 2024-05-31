#!/bin/bash
DATE=$(date +"%Y-%m-%d")
SQL_FILE=db-${MYSQL_DATABASE}-${DATE}.sql

cp ./"${SQL_FILE}" /mnt/nfs/dev/volume/sql/
