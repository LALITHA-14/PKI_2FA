from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import pyotp

app = FastAPI(title="PKI-2FA Service")

# ---------- Request Models ----------
class DecryptSeedRequest(BaseModel):
    encrypted_seed: str  # in a real scenario, this will be decrypted

class Verify2FARequest(BaseModel):
    code: str

# ---------- Paths ----------
DATA_DIR = "/app/data"
SEED_FILE = os.path.join(DATA_DIR, "seed.txt")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# ---------- Routes ----------
@app.get("/")
def root():
    return {"status": "PKI-2FA service running"}

@app.post("/decrypt-seed")
def decrypt_seed_api(payload: DecryptSeedRequest):
    """
    Simulate seed decryption. Writes a fixed seed to SEED_FILE.
    """
    try:
        # Demo seed
        seed = "JBSWY3DPEHPK3PXP"
        with open(SEED_FILE, "w") as f:
            f.write(seed)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decryption failed: {str(e)}")

@app.get("/generate-2fa")
def generate_2fa():
    """
    Generate a TOTP code using the stored seed.
    """
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed unavailable")

    try:
        with open(SEED_FILE, "r") as f:
            seed = f.read().strip()

        totp = pyotp.TOTP(seed)
        return {"code": totp.now()}  # consistent key for verification
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating TOTP: {str(e)}")

@app.post("/verify-2fa")
def verify_2fa_api(payload: Verify2FARequest):
    """
    Verify the TOTP code.
    """
    if not payload.code:
        raise HTTPException(status_code=400, detail="Missing code")

    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed unavailable")

    try:
        with open(SEED_FILE, "r") as f:
            seed = f.read().strip()

        totp = pyotp.TOTP(seed)
        # allow ±1 step (30s) for clock drift
        is_valid = totp.verify(payload.code, valid_window=1)
        return {"valid": is_valid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verifying TOTP: {str(e)}")
