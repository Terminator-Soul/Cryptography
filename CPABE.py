from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os


# Generate RSA keys for attributes
def generate_rsa_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key


# Encrypt the AES key with RSA public key
def encrypt_aes_key(aes_key, public_key):
    return public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


# Decrypt the AES key with RSA private key
def decrypt_aes_key(encrypted_aes_key, private_key):
    return private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


# Encrypt the message with AES
def encrypt_message(message, aes_key):
    iv = os.urandom(16)  # Initialization vector
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message) + encryptor.finalize()
    return iv, ciphertext


# Decrypt the message with AES
def decrypt_message(iv, ciphertext, aes_key):
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


def main():
    # Step 1: Generate RSA keys for attributes
    attr_private_key, attr_public_key = generate_rsa_key()

    # Step 2: Generate AES key
    aes_key = os.urandom(32)  # AES key for encryption

    # Step 3: Encrypt AES key using the public key of the attributes
    encrypted_aes_key = encrypt_aes_key(aes_key, attr_public_key)

    # Step 4: Encrypt the message using the AES key
    message = b"Confidential Data"
    iv, ciphertext = encrypt_message(message, aes_key)
    print(f"Ciphertext: {ciphertext}")

    # Step 5: Decrypt AES key using the private key
    decrypted_aes_key = decrypt_aes_key(encrypted_aes_key, attr_private_key)

    # Step 6: Decrypt the message using the decrypted AES key
    decrypted_message = decrypt_message(iv, ciphertext, decrypted_aes_key)
    print(f"Decrypted Message: {decrypted_message}")


if __name__ == "__main__":
    main()
