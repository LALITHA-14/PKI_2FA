import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def decrypt_seed(encrypted_seed_b64, private_key):
    encrypted_bytes = base64.b64decode(encrypted_seed_b64)

    decrypted = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    seed = decrypted.decode().strip()

    if len(seed) != 64:
        raise ValueError("Invalid seed length")

    return seed
