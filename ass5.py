# Diffie-Hellman Key Exchange with MITM Attack

p = 23
g = 5

# Alice and Bob choose private keys
a = 6
b = 15

# Eve chooses two private keys for the attack
eve_a = 7
eve_b = 9

print("Public prime p =", p)
print("Public generator g =", g)

# Step 1: Alice and Bob generate public keys
A = pow(g, a, p)
B = pow(g, b, p)

print("\n--- Normal Diffie-Hellman ---")
print("Alice's public key:", A)
print("Bob's public key:", B)

# Both calculate the same shared secret
alice_key = pow(B, a, p)
bob_key = pow(A, b, p)

print("Alice's shared key:", alice_key)
print("Bob's shared key:", bob_key)
print("Keys match:", alice_key == bob_key)

# Step 2: Eve intercepts and replaces public keys
E1 = pow(g, eve_a, p)
E2 = pow(g, eve_b, p)

print("\n--- Man-in-the-Middle Attack ---")
print("Eve sends to Alice:", E2)
print("Eve sends to Bob:", E1)

# Alice thinks E2 came from Bob
alice_mitm_key = pow(E2, a, p)

# Bob thinks E1 came from Alice
bob_mitm_key = pow(E1, b, p)

# Eve calculates the corresponding shared keys
eve_alice_key = pow(A, eve_b, p)
eve_bob_key = pow(B, eve_a, p)

print("Alice's key:", alice_mitm_key)
print("Eve's key with Alice:", eve_alice_key)

print("Bob's key:", bob_mitm_key)
print("Eve's key with Bob:", eve_bob_key)

print("Eve matches Alice's key:",
      alice_mitm_key == eve_alice_key)

print("Eve matches Bob's key:",
      bob_mitm_key == eve_bob_key)
