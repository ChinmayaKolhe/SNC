from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Shared secret key (available to both Alice and Bob)
shared_key = get_random_bytes(16)

# Alice reads the image
with open("image.jpg", "rb") as f:
    image = f.read()

# Alice encrypts the image
cipher = AES.new(shared_key, AES.MODE_GCM)
encrypted, tag = cipher.encrypt_and_digest(image)

# Alice sends nonce + tag + encrypted image
with open("encrypted.bin", "wb") as f:
    f.write(cipher.nonce + tag + encrypted)

print("Alice: Image encrypted and sent")

# Bob receives encrypted data
with open("encrypted.bin", "rb") as f:
    data = f.read()

nonce = data[:16]
tag = data[16:32]
encrypted = data[32:]

# Bob decrypts using the same shared key
try:
    decipher = AES.new(shared_key, AES.MODE_GCM, nonce=nonce)
    decrypted = decipher.decrypt_and_verify(encrypted, tag)

    with open("decrypted.jpg", "wb") as f:
        f.write(decrypted)

    print("Bob: Image decrypted successfully")
    print("Image matches:", image == decrypted)

except ValueError:
    print("Security alert: Invalid key or modified image")
