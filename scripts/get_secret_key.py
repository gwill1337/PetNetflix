import secrets

def get_key():
    return secrets.token_hex()

print(get_key())