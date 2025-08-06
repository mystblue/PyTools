# -*- coding: utf-8 -*-

__author__ = "mystblue"
__version__ = "0.1.0"
__email__ = "mysterious.blue.star@gmail.com"

import dropbox
from dropbox.files import WriteMode
import os
import shutil

def download():
    #dbx = dropbox.Dropbox(ACCESS_TOKEN)
    dbx = dropbox.Dropbox(
        app_key='5zjq0g87womfhmx',
        app_secret='cp94ttjq87qbub6',
        oauth2_refresh_token='Hf7u7G-sL-UAAAAAAAAAAbAlWR2DicBJ8U8rWxPg1tR2U20LT4Td_6OaBJN4CzqR'
    )
    metadata, res = dbx.files_download("/persona5r.zip")
    with open("persona5r.zip", 'wb') as f:
        f.write(res.content)

def backup_file():
    os.rename("persona5r", "backup_persona5r") 

def unzip():
    shutil.unpack_archive('persona5r.zip', '.')

def delete_file():
    os.remove('persona5r.zip')

if __name__ == '__main__':
    backup_file()
    download()
    unzip()
    delete_file()
