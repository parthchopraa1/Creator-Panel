from .config import get_fernet

def encrypt_token(plain: str) -> str:
    f = get_fernet()
    return f.encrypt(plain.encode()).decode()

def decrypt_token(enc: str) -> str:
    f = get_fernet()
    return f.decrypt(enc.encode()).decode()
