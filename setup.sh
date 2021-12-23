#!/bin/bash
pip3 install -r requirements.txt
cp ./awskey.py /usr/local/bin/awskey
chmod +x /usr/local/bin/awskey
exec $SHELL