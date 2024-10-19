#!/bin/bash
DATE=$(date +"%Y-%m-%d")
SQL_FILE=db-rebs-${DATE}.sql

cp "${SQL_FILE}" ../../../dev/volume/sql/
