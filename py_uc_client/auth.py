import hashlib
import base64
import time

def _md5(s):
    return hashlib.md5(s).hexdigest()

def uc_authcode(string, operation='DECODE', key='', expiry=0):
    ckey_length = 4
    key_bytes = key.encode('latin-1') if key else b''
    key_md5 = _md5(key_bytes if key_bytes else b'')
    keya = _md5(key_md5[:16].encode('latin-1'))
    keyb = _md5(key_md5[16:32].encode('latin-1'))
    if operation == 'DECODE':
        keyc = string[:ckey_length]
    else:
        keyc = _md5(str(time.time()).encode('latin-1'))[-ckey_length:]
    cryptkey = (keya + _md5((keya + keyc).encode('latin-1')))
    key_length = len(cryptkey)
    if operation == 'DECODE':
        try:
            string_bytes = base64.b64decode(string[ckey_length:].encode('latin-1'))
        except Exception:
            return ''
    else:
        expiry_time = ('%010d' % (expiry + int(time.time()) if expiry else 0)).encode('latin-1')
        md5_sum = hashlib.md5((string + keyb).encode('latin-1')).hexdigest()[:16].encode('latin-1')
        string_bytes = expiry_time + md5_sum + string.encode('latin-1')
    box = list(range(256))
    rndkey = [0] * 256
    for i in range(256):
        rndkey[i] = ord(cryptkey[i % key_length])
    j = 0
    for i in range(256):
        j = (j + box[i] + rndkey[i]) % 256
        box[i], box[j] = box[j], box[i]
    a = j = 0
    result = bytearray()
    for i in range(len(string_bytes)):
        a = (a + 1) % 256
        j = (j + box[a]) % 256
        box[a], box[j] = box[j], box[a]
        result.append(string_bytes[i] ^ box[(box[a] + box[j]) % 256])
    if operation == 'DECODE':
        try:
            result_str = result.decode('latin-1')
        except Exception:
            return ''
        if ((int(result_str[:10]) == 0 or int(result_str[:10]) - int(time.time()) > 0) and
            result_str[10:26] == hashlib.md5((result_str[26:] + keyb).encode('latin-1')).hexdigest()[:16]):
            return result_str[26:]
        return ''
    else:
        encoded = base64.b64encode(bytes(result)).decode('latin-1').replace('=', '')
        return keyc + encoded