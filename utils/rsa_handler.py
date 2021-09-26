from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.PublicKey import RSA
import base64


def encrypt_data(msg, key):
    public_key = RSA.importKey(key)
    cipher = PKCS1_cipher.new(public_key)
    encrypt_text = base64.b64encode(cipher.encrypt(bytes(msg.encode('utf8'))))
    return encrypt_text.decode('utf-8')


