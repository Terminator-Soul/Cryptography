from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64


def e_m(m, k):
    c = DES.new(k, DES.MODE_CBC)
    p_m = pad(m.encode(), DES.block_size)
    ct = c.encrypt(p_m)
    iv = c.iv
    return base64.b64encode(iv + ct).decode("utf-8")


def d_m(e_m, k):
    e_m = base64.b64decode(e_m)
    iv = e_m[: DES.block_size]
    ct = e_m[DES.block_size :]
    c = DES.new(k, DES.MODE_CBC, iv)
    p_m = c.decrypt(ct)
    m = unpad(p_m, DES.block_size)
    return m.decode("utf-8")


k = b"abcdefgh"
m = "Hello, World!"
ed_m = e_m(m, k)
dd_m = d_m(ed_m, k)
print(f"Encrypted Message:{ed_m}\nDecrypted Message:{dd_m}")
