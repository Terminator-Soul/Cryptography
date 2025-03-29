import hmac
import hashlib
from cryptography.fernet import Fernet


def g_k():
    return Fernet.generate_key()


def e_t(t, k):
    f = Fernet(k)
    e_t = f.encrypt(t).encode()
    return e_t


def d_t(e_t, k):
    f = Fernet(k)
    d_t = Fernet.decrypt(e_t).decode()
    return d_t


def c_h(k, m):
    return hmac.new(k, m, hashlib.sha256).hexdigest()


def v_h(k, m, p_h):
    e_h = c_h(k, m)
    return hmac.compare_digest(e_h, p_h)


e_k = g_k()
h_k = hashlib.sha256(e_k).digest()
i_t = "Hello this is a sample text"
ed_t = e_t(i_t, e_k)
ed_h = c_h(h_k, ed_t)
dd_t = d_t(ed_t, e_k)
if v_h(h_k, ed_t, e_k):
    print("HMAC Verificaton Passed")
else:
    print("HMAC Verificaton Failed")
print(f"Original:{i_t}")
print(f"Encrypted text:{ed_t}")
print(f"Decrypted text:{dd_t}")
print(f"Encrypted HMAC:{ed_h}")
