# -*- coding: utf-8 -*-

__author__ = "mystblue"
__version__ = "0.1.0"
__email__ = "mysterious.blue.star@gmail.com"

import dropbox
from dropbox.files import WriteMode
import os
import shutil

ACCESS_TOKEN = 'sl.u.AF6WDoe141ygKFjQXv_91GWT86plXeOJb84vQr20oH_7ekm7OOvzbgnwnzuXz-GZ2ALbMJr4_-Ryn-_wvwQrNgq_DJQoUfp5w9qRPQtEGT0ROGHhp-ZpA8eekPLQEJv-h00dfD_5-pGf6kdhzX4lkCbjX-D6caEjOlu2OgJteSvGIiu_b1vVgWzwIi12-DjeEUdh6GuOPq1WzaoFMRJJ99rgvaUTjg7QaJvLvXFt9uV6JMSrY7gk-xMibjNTqhe1lFkZ7AvAMxu_m1tUZGu5WL0RZzhUSDHdS_vGiNbsQWZR04I07m--Hnk4wqkiAXdOqyduWlqT5fgtZgb_XXibOUbDTvTeZWqbFuh4x0YVVQ4X84oUiDj83ACyyCA8IfDRzAVJSOqPaAycHJO0lD2EwT94C61A2pToLYvzUKfKPeXf-Kd3w00DSVmv3qkUMZtIJ3BG5HJDfBbY5wDgZEuzTTAxXQ-Xjy9-cIHxMcEJIvv0EQTfQzp0zVNVDevaCm0tFk8AfVZg_6i8N4gHMqjoDAaK3lY1ZZ-7opzW-nnGc4FriSS7uqtVt3hABX_A_dUVKutz12gSVv39g1iidEccSTo-sPBnVqJjYrlGURFCaVOVXmE2ViZ9FyUGZTQOaJ2FC9rl1LsCTO0eFA_iJM_VGteGw_CVhzv5gD9tN91gmRWFUeoetKDovgpsVzzIBaNvx_qPxtiZtbVpsFKse369NS0cO7o4Q3nwlmsWSoMbPXNc7spaVHEeOgyfpfMY28-xThyKWjARA8giSis7DjPbAX-42r_-snI9zd-EA-eOjL8Kay0DVbYmbPy9lZh7uE7dV0EzsB3uKURsEufP60GlCpius90sEcg_PYFOo2wOJPsyvcGPq4VmdhtglRuUsgWNF_ZOkwrur5K0pfyAAVbm9gZ2vnjKei4fMOp6c63y06_1XIOn7Mkf0RWWBaGxUHDPEV-9CFeBTvhh9P7EwNLuoL9CNX4Aw4WamaahfAxqTysi9MF6eXHxG3e81iyA77RPbdNRXH7OQxfvv-j6sfahIZz3OdtXKKQxbiT4YT_MQh7RNAIw_YM7fDUU1pHC9nl9oFGCS0kgMQfw22DjcQOtQoCvxyA8iRAX8ywiqtvsAqQQs4yoS_CzyAeAjfJrGiSHd7yYkRzP02YooxMGiASt4oMa1g7QpBUO1NBTNyp1VGLvGn4TMdC8n8zYk1SFFLgr5YuB0XtzqRXhlF_fR55vNFCmyguC7-o3l8RaISplobnQmccOm3UmEUGq-JG7Orm2fFUQR41QiJwpLu3iYdJZ8xiW'

def zip():
    shutil.make_archive('persona5r', format='zip', root_dir='.', base_dir='persona5r')

def upload():
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    with open('persona5r.zip', 'rb') as f:
        dbx.files_upload(f.read(), '/persona5r.zip', mode=WriteMode.overwrite)

def delete_file():
    os.remove('persona5r.zip')

if __name__ == '__main__':
    zip()
    upload()
    delete_file()
