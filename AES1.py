from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64


def e_m(m, k):
    c = AES.new(k, AES.MODE_CBC)
    ct_b = c.encrypt(pad(m.encode(), AES.block_size))
    iv = c.iv
    return base64.b64encode(iv + ct_b).decode("utf-8")


def d_m(e_m, k):
    e_m = base64.b64decode(e_m)
    c = AES.new(k, AES.MODE_CBC, e_m[:16])
    return unpad(c.decrypt(e_m[16:]), AES.block_size).decode("utf-8")


k = get_random_bytes(16)
m = "Keerthes"
ed_m = e_m(m, k)
dd_m = d_m(ed_m, k)
print(f"Encrypted Message:{ed_m}\nDecrypted Message:{dd_m}")
