#!/bin/bash
DATE=$(date +"%Y-%m-%d")
SQL_FILE=backup-${DATE}.sql

# 파일 존재 여부 확인
if [ -f "${SQL_FILE}" ]; then
    # 디렉토리 존재 여부 확인 및 없으면 생성
    DEST_DIR=../../../dev/volume/backups/
    if [ ! -d "${DEST_DIR}" ]; then
        mkdir -p "${DEST_DIR}"
    fi

    # 파일 복사
    cp "${SQL_FILE}" "${DEST_DIR}"
    echo "File ${SQL_FILE} copied to ${DEST_DIR}"
else
    echo "File ${SQL_FILE} does not exist."
fi
