import json
from py_uc_client.client import UCClient

UC_CONNECT = 'default'
UC_STANDALONE = 0
UC_AVTURL = ''
UC_AVTPATH = ''
UC_KEY = 'Z1mfdafsfjhofdiuhaoufhefonaf6q0s2Be4embDeN7j8Ed84A6geCcB1Yb0c'
UC_API = 'http://192.168.10.139:8080/uc_server'
UC_CHARSET = 'utf-8'
UC_IP = ''
UC_APPID = '2'
UC_PPP = '20'
UC_CLIENT_RELEASE = '20250901'

print('1. 准备加载 uc_client...')
client = UCClient(UC_API, UC_KEY, UC_APPID, UC_CLIENT_RELEASE, user_agent='UCPython/1.0', uc_ip=UC_IP)
print('2. uc_client 加载成功！')
result = client.uc_user_login('admin', 'admin', 0, 0, '', '')
print('4. 登录测试结果: ' + json.dumps(result, ensure_ascii=False))