#!/bin/bash
DATE=$(date +"%Y-%m-%d")
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
SQL_FILE="${SCRIPT_DIR}/backup-${DATE}.sql"

mariadb -u"${USER}" -p"${PASSWORD}" "${DATABASE}" < "${SQL_FILE}"

# 복원 성공 여부 확인
if [ $? -eq 0 ]; then
    echo "Database restoration completed successfully: ${SQL_FILE}"
else
    echo "Database restoration failed"
fi
