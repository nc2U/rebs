#!/bin/bash

# cert create
certbot certonly --manual --preferred-challenges=dns --email $ADMIN_EMAIL \
--server https://acme-v02.api.letsencrypt.org/directory --agree-tos -d $SERVER_NAME -d *.$SERVER_NAME
