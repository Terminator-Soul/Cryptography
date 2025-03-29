from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad
import base64


def e_m(k, m):
    c = Blowfish.new(k, Blowfish.MODE_ECB)
    p_t = pad(m.encode(), Blowfish.block_size)
    e_t = c.encrypt(p_t)
    return base64.b64encode(e_t).decode("utf-8")


def d_m(k, e_m):
    c = Blowfish.new(k, Blowfish.MODE_ECB)
    e_m = base64.b64decode(e_m)
    p_m = c.decrypt(e_m)
    m = unpad(p_m, Blowfish.block_size)
    return m.decode("utf-8")


k = b"mysecretkey"
m = "Hello, World!"
ed_m = e_m(k, m)
dd_m = d_m(k, ed_m)
print(f"Encrypted Message:{ed_m}\nDecrypted Message:{dd_m}")
