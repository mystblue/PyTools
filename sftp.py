import os
import paramiko
from paramiko.ssh_exception import BadHostKeyException, BadAuthenticationType, AuthenticationException, SSHException

# 定数
HOSTNAME = "10.200.91.131"
USERNAME = "root"
PASSWORD = "pcireadycloud"
REMOTEDIR = "/etc/nginx/conf.d/"
REMOTEFILE = "php.conf"
LOCALDIR = ""
LOCALFILE = "php.conf"


def ssh_connect(host_name, user_name, passwd):
    """
    SSH接続
    """
    client = paramiko.client.SSHClient()
    #  HostKyeの読み込み
    client.load_system_host_keys()
    #  HostKeyがない場合にHost名とHostKyeを保存
    client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
    try:
        client.connect(hostname=host_name, username=user_name, password=passwd, timeout=10, auth_timeout=30)
    except BadHostKeyException:
        # hostkeyの不一致
        print("The host key given by the SSH server did not match what we were expecting.")
    except BadAuthenticationType:
        # 認証タイプが許可されていない（パスワード認証が許可されていないなど）
        print("Exception raised when an authentication type is used, but the server isn’t allowing that type.")
    except SSHException:
        # sshプロトコルの失敗
        print("Exception raised by failures in SSH2 protocol negotiation or logic errors.")
    except AuthenticationException:
        # 不明なエラーで認証に失敗
        print("Exception raised when authentication failed for some reason")
    return client
    
def sftp_download(host_name, user_name, passwd, remote_file, local_file):
    """
    SFTPダウンロード
    """
    # ssh接続
    with ssh_connect(host_name, user_name, passwd) as client:
        # sftp
        with client.open_sftp() as sftp:
            # ダウンロード
            sftp.get(remotepath=remote_file, localpath=local_file)
    return
                
if __name__ == '__main__':
    if not os.path.exists("stg"):
        os.makedirs("stg")
    if not os.path.exists("dev"):
        os.makedirs("dev")

    # TMS の php.conf
    data = ["10.200.91.131", "root", "pcireadycloud", "/etc/nginx/conf.d/php.conf", "stg\\tms_php.conf"]
    sftp_download(data[0], data[1], data[2], data[3], data[4])
    
    data = ["10.200.91.9", "root", "pcireadycloud", "/etc/nginx/conf.d/php.conf", "dev\\tms_php.conf"]
    sftp_download(data[0], data[1], data[2], data[3], data[4])

    # TMS の php.ini
    data = ["10.200.91.131", "root", "pcireadycloud", "/etc/php.ini", "stg\\tms_php.ini"]
    sftp_download(data[0], data[1], data[2], data[3], data[4])
    
    data = ["10.200.91.9", "root", "pcireadycloud", "/etc/php.ini", "dev\\tms_php.ini"]
    sftp_download(data[0], data[1], data[2], data[3], data[4])

    # TMS の www.conf
    data = ["10.200.91.131", "root", "pcireadycloud", "/etc/php-fpm.d/www.conf", "stg\\tms_www.conf"]
    sftp_download(data[0], data[1], data[2], data[3], data[4])
    
    data = ["10.200.91.9", "root", "pcireadycloud", "/etc/php-fpm.d/www.conf", "dev\\tms_www.conf"]
    sftp_download(data[0], data[1], data[2], data[3], data[4])



    # TMSWEB の php.conf
    data = ["10.200.91.151", "root", "pcireadycloud", "/etc/nginx/conf.d/php.conf", "stg\\tmsweb_php.conf"]
    sftp_download(data[0], data[1], data[2], data[3], data[4])
    
    data = ["10.200.91.10", "root", "pcireadycloud", "/etc/nginx/conf.d/php.conf", "dev\\tmsweb_php.conf"]
    sftp_download(data[0], data[1], data[2], data[3], data[4])

    # TMSWEB の php.ini
    data = ["10.200.91.151", "root", "pcireadycloud", "/etc/php.ini", "stg\\tmsweb_php.ini"]
    sftp_download(data[0], data[1], data[2], data[3], data[4])
    
    data = ["10.200.91.10", "root", "pcireadycloud", "/etc/php.ini", "dev\\tmsweb_php.ini"]
    sftp_download(data[0], data[1], data[2], data[3], data[4])

    # TMSWEB の www.conf
    data = ["10.200.91.151", "root", "pcireadycloud", "/etc/php-fpm.d/www.conf", "stg\\tmsweb_www.conf"]
    sftp_download(data[0], data[1], data[2], data[3], data[4])
    
    data = ["10.200.91.10", "root", "pcireadycloud", "/etc/php-fpm.d/www.conf", "dev\\tmsweb_www.conf"]
    sftp_download(data[0], data[1], data[2], data[3], data[4])



    # GW の php.conf
    data = ["10.200.91.141", "root", "pcireadycloud", "/etc/nginx/conf.d/php.conf", "stg\\gw_php.conf"]
    sftp_download(data[0], data[1], data[2], data[3], data[4])
    
    data = ["10.200.91.8", "root", "pcireadycloud", "/etc/nginx/conf.d/php.conf", "dev\\gw_php.conf"]
    sftp_download(data[0], data[1], data[2], data[3], data[4])

    # GW の php.ini
    data = ["10.200.91.141", "root", "pcireadycloud", "/etc/php.ini", "stg\\gw_php.ini"]
    sftp_download(data[0], data[1], data[2], data[3], data[4])
    
    data = ["10.200.91.8", "root", "pcireadycloud", "/etc/php.ini", "dev\\gw_php.ini"]
    sftp_download(data[0], data[1], data[2], data[3], data[4])

    # GW の www.conf
    data = ["10.200.91.141", "root", "pcireadycloud", "/etc/php-fpm.d/www.conf", "stg\\gw_www.conf"]
    sftp_download(data[0], data[1], data[2], data[3], data[4])
    
    data = ["10.200.91.8", "root", "pcireadycloud", "/etc/php-fpm.d/www.conf", "dev\\gw_www.conf"]
    sftp_download(data[0], data[1], data[2], data[3], data[4])
