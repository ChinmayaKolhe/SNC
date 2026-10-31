import hashlib

# Function to calculate SHA-1 digest
def calculate_sha1(text):
    sha1 = hashlib.sha1(text.encode('utf-8'))
    return sha1.hexdigest()


# Accept both texts from the user
original_text = input("Enter the original text: ")
modified_text = input("Enter the modified text: ")

# Calculate digests
original_digest = calculate_sha1(original_text)
modified_digest = calculate_sha1(modified_text)

# Display results
print("\nOriginal Text:", original_text)
print("Original SHA-1 Digest:", original_digest)

print("\nModified Text:", modified_text)
print("Modified SHA-1 Digest:", modified_digest)

# Compare both digests
if original_digest == modified_digest:
    print("\nBoth digests match.")
else:
    print("\nDigests are different. Input has changed.")
