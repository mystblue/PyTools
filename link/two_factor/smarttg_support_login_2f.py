import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import totp
#from selenium.webdriver.common.alert import Alert

options = webdriver.ChromeOptions()
#options.add_argument('--headless=new')
options.add_argument("--ignore-urlfetcher-cert-requests")
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.accept_insecure_certs = True

driver = webdriver.Chrome(options=options)

#options = webdriver.FirefoxOptions()
#options.add_argument('--headless=new')
#options.add_argument("--ignore-urlfetcher-cert-requests")
#options.add_argument('--disable-gpu')
#options.add_argument('--no-sandbox')
#options.accept_insecure_certs = True

#driver = webdriver.Firefox(options=options)

driver.get('https://support.smarttg.jp/wp-login.php')
# アクセス先のURLを出力
#print(driver.current_url)

#ログイン
element = driver.find_element(By.ID, "user_login")
element.send_keys('')
time.sleep(2)
element = driver.find_element(By.ID, "user_pass")
element.send_keys('')
time.sleep(2)

check_input = driver.find_element(By.ID, "wp-submit").click()
URL = driver.current_url
assert 'https://support.smarttg.jp/wp-login.php' == URL,"URLs are different!"

# 認証コード入力
auth_secret = ''
seed = base64.b32decode(auth_secret)
#print(f"{auth_secret}: {seed}")
totp_value = totp.generate_totp(seed, totp.get_current_steps())
element = driver.find_element(By.ID, "authcode")
element.send_keys(totp_value)
time.sleep(3)
#while URL == 'https://support.smarttg.jp/wp-login.php':
#    URL = driver.current_url
URL = driver.current_url
assert 'https://support.smarttg.jp/' == URL,"URLs are different!"

#メニュー
check_input = driver.find_element(By.XPATH, "//a[contains(@title, 'お問い合わせ')]").click()
URL = driver.current_url
assert 'https://support.smarttg.jp/inquiry/' == URL,"URLs are different!"

#ログアウト
check_input = driver.find_element(By.XPATH, "//a[@title='ログアウト']").click()
URL = driver.current_url
assert 'https://support.smarttg.jp/wp-login.php?action=logout' == URL,"URLs are different!"
check_input = driver.find_element(By.XPATH, "//a[text()='ログアウト']").click()
URL = driver.current_url
assert 'https://support.smarttg.jp/wp-login.php?loggedout=true&wp_lang=ja' == URL,"URLs are different!"

#v = input("続行するには何かキーを押してください > ")
driver.quit()
print("正常終了")
