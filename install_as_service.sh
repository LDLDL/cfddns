#! bash
python3 ./init.py
mkdir /srv/cfddns
cp cfddns.py /srv/cfddns/
cp conf.json /srv/cfddns/
cp cfddns.service /usr/lib/systemd/system/
touch /srv/cfddns/cfddns.log
systemctl daemon-reload
systemctl enable cfddns
systemctl start cfddns
