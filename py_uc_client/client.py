import hashlib
import time
from urllib import request, parse

from .auth import uc_authcode
from .xmlcodec import uc_unserialize


class UCClient:
    def __init__(self, uc_api, uc_key, uc_appid, release, user_agent='UCPython/1.0', uc_ip=''):
        self.uc_api = uc_api.rstrip('/')
        self.uc_key = uc_key
        self.uc_appid = str(uc_appid)
        self.release = str(release)
        self.user_agent = user_agent
        self.uc_ip = uc_ip

    def _agent_md5(self):
        return hashlib.md5(self.user_agent.encode('latin-1')).hexdigest()

    def uc_api_input(self, data, module, action):
        s = data + f"&m={module}&a={action}&appid={self.uc_appid}"
        payload = s + f"&agent={self._agent_md5()}&time={int(time.time())}"
        encoded = uc_authcode(payload, 'ENCODE', self.uc_key, 0)
        return parse.quote(encoded, safe='')

    def uc_api_requestdata(self, module, action, arg, extra=''):
        input_str = self.uc_api_input(arg, module, action)
        return f"m={module}&a={action}&inajax=2&release={self.release}&input={input_str}&appid={self.uc_appid}{extra}"

    def _build_arg_string(self, arg_dict):
        items = []
        for k, v in arg_dict.items():
            k_enc = parse.quote(str(k), safe='')
            if isinstance(v, dict):
                for k2, v2 in v.items():
                    k2_enc = parse.quote(str(k2), safe='')
                    v2_enc = parse.quote(str(v2), safe='')
                    items.append(f"{k_enc}[{k2_enc}]={v2_enc}")
            else:
                items.append(f"{k_enc}={parse.quote(str(v), safe='')}")
        return '&'.join(items)

    def uc_api_post(self, module, action, arg):
        s = self._build_arg_string(arg)
        postdata = self.uc_api_requestdata(module, action, s)
        url = f"{self.uc_api}/index.php"
        data_bytes = postdata.encode('latin-1')
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': self.user_agent,
        }
        req = request.Request(url, data=data_bytes, headers=headers, method='POST')
        with request.urlopen(req, timeout=20) as resp:
            return resp.read()

    def uc_user_login(self, username, password, isuid=0, checkques=0, questionid='', answer='', ip='', nolog=0):
        args = {
            'username': username,
            'password': password,
            'isuid': int(isuid),
            'checkques': int(checkques),
            'questionid': questionid,
            'answer': answer,
            'ip': ip,
            'nolog': int(nolog),
        }
        resp = self.uc_api_post('user', 'login', args)
        return uc_unserialize(resp)