# -*- coding: utf-8 -*-

__author__ = "mystblue"
__version__ = "0.1.0"
__email__ = "mysterious.blue.star@gmail.com"

import dropbox
from dropbox.files import WriteMode
import os
import shutil

def zip():
    shutil.make_archive('persona5r', format='zip', root_dir='.', base_dir='persona5r')

def upload():
    #dbx = dropbox.Dropbox(ACCESS_TOKEN)
    dbx = dropbox.Dropbox(
        app_key='5zjq0g87womfhmx',
        app_secret='cp94ttjq87qbub6',
        oauth2_refresh_token='Hf7u7G-sL-UAAAAAAAAAAbAlWR2DicBJ8U8rWxPg1tR2U20LT4Td_6OaBJN4CzqR'
    )

    with open('persona5r.zip', 'rb') as f:
        dbx.files_upload(f.read(), '/persona5r.zip', mode=WriteMode.overwrite)

def delete_file():
    os.remove('persona5r.zip')

if __name__ == '__main__':
    zip()
    upload()
    delete_file()
