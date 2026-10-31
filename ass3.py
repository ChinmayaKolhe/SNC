import time
from math import gcd
from sympy import randprime

# Generate RSA keys
def generate_keys(bits):
    while True:
        p = randprime(2**(bits//2 - 1), 2**(bits//2))
        q = randprime(2**(bits//2 - 1), 2**(bits//2))

        if p == q:
            continue

        n = p * q
        phi = (p - 1) * (q - 1)
        e = 65537

        if gcd(e, phi) == 1:
            d = pow(e, -1, phi)
            return e, d, n


# RSA encryption: C = M^e mod n
def encrypt(message, e, n):
    return pow(message, e, n)


# RSA decryption: M = C^d mod n
def decrypt(cipher, d, n):
    return pow(cipher, d, n)


# Experiment
key_sizes = [128, 256, 512, 1024]
message_sizes = [8, 16, 32, 64]
runs = 100

for bits in key_sizes:

    # Key generation time
    start = time.perf_counter()
    e, d, n = generate_keys(bits)
    key_time = time.perf_counter() - start

    print("\nRSA Key Size:", bits, "bits")
    print("Key Generation Time:", round(key_time, 6), "seconds")

    for size in message_sizes:

        # Message must be smaller than n
        message = (1 << size) - 1

        if message >= n:
            print("Message too large:", size, "bits")
            continue

        # Encryption time
        start = time.perf_counter()

        for _ in range(runs):
            cipher = encrypt(message, e, n)

        enc_time = (time.perf_counter() - start) / runs

        # Decryption time
        start = time.perf_counter()

        for _ in range(runs):
            plain = decrypt(cipher, d, n)

        dec_time = (time.perf_counter() - start) / runs

        print("\nMessage Size:", size, "bits")
        print("Encryption Time:", round(enc_time, 8), "seconds")
        print("Decryption Time:", round(dec_time, 8), "seconds")
        print("Correct:", plain == message)