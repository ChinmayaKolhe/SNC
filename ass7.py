from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

# Step 1: Take input from the user
message = input("Enter the original tender message: ")
modified_message = input("Enter the modified message: ")

# Step 2: Generate DSA private and public keys
private_key = dsa.generate_private_key(key_size=2048)
public_key = private_key.public_key()

print("\nDSA key pair generated successfully.")

# Step 3: Sign the original message using the private key
signature = private_key.sign(
    message.encode("utf-8"),
    hashes.SHA256()
)

print("\nOriginal Message:", message)
print("Digital Signature (Hex):", signature.hex())

# Step 4: Verify the original message
print("\n--- Verification of Original Message ---")

try:
    public_key.verify(
        signature,
        message.encode("utf-8"),
        hashes.SHA256()
    )
    print("Signature is VALID.")
    print("Authentication and integrity checks passed.")
except InvalidSignature:
    print("Signature is INVALID.")

# Step 5: Verify the modified message using the same signature
print("\n--- Verification of Modified Message ---")

try:
    public_key.verify(
        signature,
        modified_message.encode("utf-8"),
        hashes.SHA256()
    )
    print("Signature is VALID.")
except InvalidSignature:
    print("Signature is INVALID.")
    print("Message was modified or does not match the signature.")