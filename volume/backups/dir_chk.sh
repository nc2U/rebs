#!/bin/bash
mysql_name="./volume/mysql/"
if ! test -d $mysql_name
then mkdir $mysql_name

media_name="./app/django/media/"
if ! test -d $media_name
then mkdir $media_name
fi
