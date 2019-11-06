import hashlib


def encrypt(val):
    val_e = val.encode('utf-8')
    return hashlib.sha512(val_e).digest()