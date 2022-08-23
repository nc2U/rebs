#!/bin/bash
DATE=`date +"%Y-%m-%d"`
SQLFILE=/var/backups/db-rebs-${DATE}.sql
DATABASE=${MYSQL_DATABASE}
USER=${MYSQL_USER}
PASSWORD=${MYSQL_PASSWORD}

# (2) in case you run this more than once a day,
# remove the previous version of the file
unalias rm     2> /dev/null
rm ${SQLFILE}     2> /dev/null
rm ${SQLFILE}.gz  2> /dev/null

# (3) do the mysql database backup (dump)
mysqldump -u${USER} -p${PASSWORD} ${DATABASE} --ignore-table=${DATABASE}.django_migrations > ${SQLFILE}
