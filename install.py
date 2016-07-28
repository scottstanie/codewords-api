#!/usr/bin/env python
import os

os.system("echo")
os.system("echo 'WOLFHOUND-SERVER INITIAL INSTALL'")
os.system("echo '================================'")
os.system("echo")

try:
    response_runupdate = raw_input('Ready to INSTALL/UPDATE ASSETS (Y/n)? ').lower()
    if response_runupdate == 'n':
        os.system("echo")
        os.system("echo 'ASSET INSTALL skipped.'")
    else:
        os.system("echo")
        os.system("echo 'INSTALLING/UPDATING setuptools...'")
        os.system("$VIRTUAL_ENV/bin/pip install --upgrade setuptools")
        os.system("echo")
        os.system("echo 'INSTALLING/UPDATING pip...'")
        os.system("$VIRTUAL_ENV/bin/pip install --upgrade pip")
        os.system("echo")
        os.system("echo 'INSTALLING/UPDATING assets...'")
        os.system("$VIRTUAL_ENV/bin/pip install \
            -r requirements.txt")

    os.system("echo")
    response_runsetup = raw_input('Ready to run SETUP (Y/n)? ').lower()
    if response_runsetup == 'n':
        os.system("echo")
        os.system("echo 'SETUP skipped.'")
    else:
        os.system("echo")
        os.system("$VIRTUAL_ENV/bin/python manage.py setup --skipassets")

except KeyboardInterrupt:
    os.system("echo")
    os.system("echo 'Operation cancelled.'")
