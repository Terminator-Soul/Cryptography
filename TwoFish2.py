from struct import pack, unpack

BLOCK_SIZE = 16
KEY_SIZE = 16

S_BOXES = [
    [
        0xD1310BA6,
        0x98DFB5AC,
        0x2FFD72DB,
        0xD01ADFB7,
        0xB8E1AFED,
        0x6A267E96,
        0xBA7C9045,
        0xF12C7F99,
        0x24A19947,
        0xB3916CF7,
        0x0801F2E2,
        0x858EFC16,
        0x636920D8,
        0x71574E69,
        0xA458FEA3,
        0xF4933D7E,
    ],
    [
        0x0D0C6E0B,
        0x0A0B0C0D,
        0x0E0F1011,
        0x0C0D0E0F,
        0x0B0C0D0E,
        0x0A0B0C0D,
        0x0F101112,
        0x0E0F1011,
        0x0C0D0E0F,
        0x0B0C0D0E,
        0x0A0B0C0D,
        0x0F101112,
        0x0E0F1011,
        0x0C0D0E0F,
        0x0B0C0D0E,
        0x0A0B0C0D,
    ],
]


class Twofish:
    def __init__(self, key):
        if len(key) != KEY_SIZE:
            raise ValueError(f"Key must be {KEY_SIZE} bytes long.")
        self.key = key
        self.subkeys = self.key_schedule(key)

    def key_schedule(self, key):
        return [key[i % len(key)] for i in range(40)]

    def encrypt(self, plaintext):
        if len(plaintext) != BLOCK_SIZE:
            raise ValueError(f"Plaintext must be {BLOCK_SIZE} bytes long.")
        ciphertext = bytearray(BLOCK_SIZE)
        for i in range(BLOCK_SIZE):
            ciphertext[i] = plaintext[i] ^ self.subkeys[i % len(self.subkeys)]
        return bytes(ciphertext)

    def decrypt(self, ciphertext):
        if len(ciphertext) != BLOCK_SIZE:
            raise ValueError(f"Ciphertext must be {BLOCK_SIZE} bytes long.")
        plaintext = bytearray(BLOCK_SIZE)
        for i in range(BLOCK_SIZE):
            plaintext[i] = ciphertext[i] ^ self.subkeys[i % len(self.subkeys)]
        return bytes(plaintext)


key = b"abcdefghijklmnop"
twofish = Twofish(key)
plaintext = b"exampleplaintext"
ciphertext = twofish.encrypt(plaintext)
print(f"Ciphertext: {ciphertext}")
decrypted = twofish.decrypt(ciphertext)
print(f"Decrypted: {decrypted}")
