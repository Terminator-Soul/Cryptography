import hmac
import hashlib
from cryptography.fernet import Fernet

encryption_key = Fernet.generate_key()
cipher = Fernet(encryption_key)

hmac_key = b"supersecretkey"

message = b"Sensitive information to protect"

encrypted_message = cipher.encrypt(message)
print(f"Encrypted Message: {encrypted_message}")


def create_hmac(key, data):
    return hmac.new(key, data, hashlib.sha256).hexdigest()


hmac_signature = create_hmac(hmac_key, encrypted_message)
print(f"HMAC Signature: {hmac_signature}")


def verify_hmac(key, data, provided_signature):
    calculated_signature = hmac.new(key, data, hashlib.sha256).hexdigest()
    return hmac.compare_digest(calculated_signature, provided_signature)


is_valid = verify_hmac(hmac_key, encrypted_message, hmac_signature)
if is_valid:
    print("HMAC verification passed")
    decrypted_message = cipher.decrypt(encrypted_message)
    print(f"Decrypted Message: {decrypted_message.decode()}")
else:
    print("HMAC verification failed")
