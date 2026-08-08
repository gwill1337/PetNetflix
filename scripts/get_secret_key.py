from hashlib import sha256
import secrets

def get_key():
    return secrets.token_hex()

def test_hash():
    
    return sha256("text".encode("utf-8")).hexdigest()

# print(get_key())
print(test_hash())