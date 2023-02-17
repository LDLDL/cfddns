#!/usr/bin/bash


if ! grep -q 'systemd' /proc/1/comm
then
    echo 'systemd not found.'
    exit 1
fi


mkdir -p /opt/cfddns
python3 ./config.py
cp conf.json /opt/cfddns/
cp cfddns.py /opt/cfddns/
cp -r sources /opt/cfddns/
cp cfddns.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable cfddns
systemctl start cfddns
