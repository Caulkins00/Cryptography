# import base64
# import os
# from cryptography.fernet import Fernet
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# password = b"password"
# salt = os.urandom(16)
# kdf = PBKDF2HMAC(
#     algorithm=hashes.SHA256(),
#     length=32,
#     salt=salt,
#     iterations=480000,
# )
# x = kdf.derive(password)
# print(x)
# key = base64.urlsafe_b64encode(x)
# f = Fernet(key)
# print(key)
# token = f.encrypt(b"Secret message!")
# print(token)
# print(f.decrypt(token))

import hashlib
import os
import getpass
from hashlib import sha256
from base64 import b64encode, b64decode
# salt = os.urandom(16)
# print("salt: " + str(salt))

password = getpass.getpass().encode(encoding='ascii')
print("password: " + str(password))
password2 = hashlib.sha256(password).hexdigest()
print("password hash: " + str(password2))
