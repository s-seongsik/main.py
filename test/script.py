import os
import binascii
from base64 import b64encode

random_bytes = binascii.hexlify(os.urandom(12))
token = b64encode(random_bytes).decode('utf-8')
