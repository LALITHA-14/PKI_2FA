from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import pyotp

app = FastAPI(title="PKI-2FA Service")

# ---------- Request Models ----------
class DecryptSeedRequest(BaseModel):
    encrypted_seed: str  # simulated encrypted input

class Verify2FARequest(BaseModel):
    code: str


# ---------- Paths (OS Independent) ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
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
    Simulate seed decryption and store the seed securely.
    """
    if not payload.encrypted_seed:
        raise HTTPException(status_code=400, detail="Encrypted seed missing")

    try:
        # Demo seed (in real PKI this would be decrypted)
        seed = "JBSWY3DPEHPK3PXP"

        with open(SEED_FILE, "w") as f:
            f.write(seed)

        return {"status": "Seed stored successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decryption failed: {str(e)}")


@app.get("/generate-2fa")
def generate_2fa():
    """
    Generate a TOTP code using stored seed.
    """
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=400, detail="Seed not initialized")

    try:
        with open(SEED_FILE, "r") as f:
            seed = f.read().strip()

        totp = pyotp.TOTP(seed)
        return {"code": totp.now()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TOTP generation error: {str(e)}")


@app.post("/verify-2fa")
def verify_2fa_api(payload: Verify2FARequest):
    """
    Verify the TOTP code.
    """
    if not payload.code:
        raise HTTPException(status_code=400, detail="Code is required")

    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=400, detail="Seed not initialized")

    try:
        with open(SEED_FILE, "r") as f:
            seed = f.read().strip()

        totp = pyotp.TOTP(seed)

        # Allow ±30 seconds window
        is_valid = totp.verify(payload.code, valid_window=1)

        return {"valid": is_valid}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification error: {str(e)}")
