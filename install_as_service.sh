#! bash
mkdir -p /opt/cfddns
python3 ./config.py
cp cfddns.py /opt/cfddns/
cp cfddns.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable cfddns
systemctl start cfddns
