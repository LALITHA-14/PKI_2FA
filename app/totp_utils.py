import base64
import pyotp
import time

def _load_seed():
    with open("data/seed.txt") as f:
        return f.read().strip()

def generate_totp():
    seed_hex = _load_seed()
    seed_bytes = bytes.fromhex(seed_hex)
    base32 = base64.b32encode(seed_bytes).decode()

    totp = pyotp.TOTP(base32, digits=6, interval=30)
    code = totp.now()
    remaining = 30 - (int(time.time()) % 30)

    return {"code": code, "valid_for": remaining}

def verify_totp(code):
    seed_hex = _load_seed()
    seed_bytes = bytes.fromhex(seed_hex)
    base32 = base64.b32encode(seed_bytes).decode()

    totp = pyotp.TOTP(base32, digits=6, interval=30)
    return totp.verify(code, valid_window=1)
