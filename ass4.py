# Custom Double-Layer Encryption Algorithm (DLSX)
def encrypt(message, key):
    ciphertext = []

    for i, ch in enumerate(message):
        # Layer 1: Position-based shifting
        shifted = (ord(ch) + key + i) % 65536

        # Layer 2: XOR operation
        encrypted = shifted ^ (key + i)

        ciphertext.append(encrypted)

    return ciphertext


def decrypt(ciphertext, key):
    message = ""

    for i, value in enumerate(ciphertext):
        # Reverse Layer 2: XOR
        shifted = value ^ (key + i)

        # Reverse Layer 1: Shift
        original = (shifted - key - i) % 65536

        message += chr(original)

    return message


# Main program
message = input("Enter plaintext: ")
key = int(input("Enter secret key (1-255): "))

if not 1 <= key <= 255:
    print("Key must be between 1 and 255.")
else:
    encrypted = encrypt(message, key)
    decrypted = decrypt(encrypted, key)

    print("\nOriginal Message:", message)
    print("Encrypted Message:", encrypted)
    print("Decrypted Message:", decrypted)
    print("Successful:", message == decrypted)