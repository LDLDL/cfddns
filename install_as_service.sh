#! bash
mkdir -p /srv/cfddns
python3 ./config.py
cp cfddns.py /srv/cfddns/
cp cfddns.service /etc/systemd/system/
touch /srv/cfddns/cfddns.log
systemctl daemon-reload
systemctl enable cfddns
systemctl start cfddns
