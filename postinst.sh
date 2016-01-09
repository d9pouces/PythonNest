#!/usr/bin/env bash
mkdir -p /var/pythonnest/gpg
chown -R pythonnest: /var/pythonnest/
chmod 0700 /var/pythonnest/gpg
sudo -u pythonnest pythonnest-manage gpg_gen generate
KEY_ID=`sudo -u pythonnest pythonnest-manage gpg_gen show | tail -n 1 | cut -f 4 -d ' ' | cut -f 1 -d ','`
sed -i "s/1DA759EA7F5EF06F/$KEY_ID/g" /etc/pythonnest/settings.ini
