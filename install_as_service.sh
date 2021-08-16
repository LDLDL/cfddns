#! bash
python3 ./init.py
mkdir /etc/cfddns
cp cfddns.py /etc/cfddns/
cp conf.json /etc/cfddns/
cp cfddns.service /usr/lib/systemd/system/
systemctl daemon-reload
systemctl enable cfddns
systemctl start cfddns