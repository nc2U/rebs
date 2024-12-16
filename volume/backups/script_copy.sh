#!/bin/bash
# 스크립트 파일이 위치한 디렉터리 경로
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

DATE=$(date +"%Y-%m-%d")
SQL_FILE="${SCRIPT_DIR}/backup-${DATE}.sql"  # 스크립트 디렉터리를 기준으로 파일 경로 설정

# 파일 존재 여부 확인
if [ -f "${SQL_FILE}" ]; then
    # 디렉토리 존재 여부 확인 및 없으면 생성
    DEST_DIR=/volume1/mnt/ibs/dev/volume/backups/
    if [ ! -d "${DEST_DIR}" ]; then
        mkdir -p "${DEST_DIR}"
    fi

    # 파일 복사
    cp "${SQL_FILE}" "${DEST_DIR}"
    echo "File ${SQL_FILE} copied to ${DEST_DIR}"
else
    echo "File ${SQL_FILE} does not exist."
fi
