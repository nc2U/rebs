#!/bin/bash
mysql_name="./volume/mysql/"
if ! test -d $mysql_name
then mkdir "./volume/mysql/"

media_name="./app/django/media/"
if ! test -d $media_name
then mkdir "./app/django/media/"
fi
