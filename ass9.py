import os
import json
import base64
import hashlib
import uuid

from cryptography.hazmat.primitives.asymmetric import (
    rsa, padding
)
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# Convert binary data into Base64
def encode(data):
    return base64.b64encode(data).decode("utf-8")


# Convert Base64 back into binary
def decode(data):
    return base64.b64decode(data)


# Generate RSA keys for a user
def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    return private_key, public_key


# Convert package fields into consistent bytes
def package_bytes(package):
    return json.dumps(
        package, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


# STEP 1: Generate keys for both users

sender_private, sender_public = generate_keys()
receiver_private, receiver_public = generate_keys()

print("RSA keys generated successfully!")


# STEP 2: SENDER - Select image

image_path = input("Enter image path: ")

if not os.path.isfile(image_path):
    raise FileNotFoundError("Image file not found!")

with open(image_path, "rb") as file:
    image_data = file.read()

print("Original image loaded successfully!")
print("Original image size:", len(image_data), "bytes")


# STEP 3: Generate AES-256 key

aes_key = AESGCM.generate_key(bit_length=256)

print("AES-256 secret key generated!")


# STEP 4: Encrypt image using AES-GCM

nonce = os.urandom(12)

message_id = str(uuid.uuid4())

aes = AESGCM(aes_key)

encrypted_image = aes.encrypt(
    nonce,
    image_data,
    message_id.encode("utf-8")
)

print("Image encrypted successfully!")


# STEP 5: Encrypt AES key using receiver's RSA public key

encrypted_aes_key = receiver_public.encrypt(
    aes_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("AES key encrypted using receiver's public key!")


# STEP 6: Prepare encrypted package

package = {
    "message_id": message_id,
    "nonce": encode(nonce),
    "encrypted_key": encode(encrypted_aes_key),
    "encrypted_image": encode(encrypted_image)
}


# STEP 7: Generate digital signature

signature = sender_private.sign(
    package_bytes(package),
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

package["signature"] = encode(signature)

print("Digital signature generated successfully!")


# STEP 8: Save package (simulate network transmission)

with open("encrypted_package.json", "w") as file:
    json.dump(package, file)

print("\nEncrypted package transmitted successfully!")
print("File: encrypted_package.json")


# STEP 9: RECEIVER - Read received package

with open("encrypted_package.json", "r") as file:
    received_package = json.load(file)

signature = decode(received_package["signature"])

# Separate signed data and signature
signed_data = {
    key: value
    for key, value in received_package.items()
    if key != "signature"
}


# STEP 10: Verify digital signature

try:
    sender_public.verify(
        signature,
        package_bytes(signed_data),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    print("\nDigital signature verified!")
    print("Sender authentication successful!")

except Exception:
    print("\nWARNING: Digital signature verification failed!")
    print("Image may have been modified.")
    raise SystemExit


# STEP 11: Decrypt AES key using receiver's private key

decrypted_aes_key = receiver_private.decrypt(
    decode(received_package["encrypted_key"]),
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("AES key decrypted successfully!")


# STEP 12: Decrypt image using AES-GCM

nonce = decode(received_package["nonce"])
ciphertext = decode(received_package["encrypted_image"])

aes = AESGCM(decrypted_aes_key)

try:
    original_image = aes.decrypt(
        nonce,
        ciphertext,
        received_package["message_id"].encode("utf-8")
    )

    print("Image integrity verified successfully!")

except Exception:
    print("Image authentication failed!")
    raise SystemExit


# STEP 13: Save original image

output_path = "received_image.jpg"

with open(output_path, "wb") as file:
    file.write(original_image)

# Calculate SHA-256 for comparison
original_hash = hashlib.sha256(image_data).hexdigest()
received_hash = hashlib.sha256(original_image).hexdigest()

print("\nSHA-256 Comparison:")
print("Original Image Hash:", original_hash)
print("Received Image Hash:", received_hash)

if original_hash == received_hash:
    print("Image integrity confirmed!")
else:
    print("Image integrity check failed!")

print("\nSecure image received successfully!")
print("Saved as:", output_path)