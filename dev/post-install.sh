#!/bin/sh

set -e

USER_EXISTS=`getent passwd pythonnest || :`
if [ -z "${USER_EXISTS}" ]; then
    useradd pythonnest -b /var/ -U -r
fi


mkdir -p /opt/pythonnest/var/media
mkdir -p /opt/pythonnest/var/data
mkdir -p /opt/pythonnest/var/log
chown -R : /opt/pythonnest


set +e

