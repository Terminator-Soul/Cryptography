from Crypto.Cipher import AES

k = b"SuperSecretKey1234567890"
c = AES.new(k, AES.MODE_EAX)
d = b"This is some sensitive data"
ct, t = c.encrypt_and_digest(d)
c = AES.new(k, AES.MODE_EAX, c.nonce)
pt = c.decrypt_and_verify(ct, t)
print(ct, "\n", pt.decode("utf-8"))
