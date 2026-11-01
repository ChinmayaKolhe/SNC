import time
from math import gcd
from sympy import randprime

def generate_keys(bits):
    while True:
        p = randprime(2 ** (bits // 2 - 1), 2 ** (bits // 2))
        q = randprime(2 ** (bits // 2 - 1), 2 ** (bits // 2))
        if p != q:
            n = p * q
            if n.bit_length() != bits:
                continue
            phi = (p - 1) * (q - 1)
            e = 65537
            if gcd(e, phi) == 1:
                return e, pow(e, -1, phi), n


key_sizes = [128, 256, 512, 1024]
message_sizes = [8, 16, 32, 64]
runs = 100

for bits in key_sizes:
    start = time.perf_counter()
    e, d, n = generate_keys(bits)
    key_time = time.perf_counter() - start

    print(f"\nKey size: {bits} bits")
    print(f"Key generation time: {key_time:.6f} seconds")

    for size in message_sizes:
        message = (1 << size) - 1

        start = time.perf_counter()
        cipher = pow(message, e, n)
        encrypt_time = time.perf_counter() - start

        start = time.perf_counter()
        plain = pow(cipher, d, n)
        decrypt_time = time.perf_counter() - start

        print(f"\nMessage size: {size} bits")
        print(f"Original message: {message}")
        print(f"Encrypted message: {cipher}")
        print(f"Decrypted message: {plain}")
        print(f"Correct: {plain == message}")
        print(f"Encryption time: {encrypt_time:.8f} seconds")
        print(f"Decryption time: {decrypt_time:.8f} seconds")
