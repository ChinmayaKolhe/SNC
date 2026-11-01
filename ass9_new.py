from cryptography.fernet import Fernet, InvalidToken
 
 # Generate shared secret key
 shared_key = Fernet.generate_key()
 
 # Alice and Bob use the same key
 alice = Fernet(shared_key)
 bob = Fernet(shared_key)
 
 # Alice reads the image
 with open("image.jpg", "rb") as f:
     image = f.read()
 
 # Alice encrypts the image
 encrypted = alice.encrypt(image)
 
 # Simulate sending encrypted image
 with open("encrypted.bin", "wb") as f:
     f.write(encrypted)
 
 print("Alice: Image encrypted and sent")
 
 # Bob receives encrypted image
 with open("encrypted.bin", "rb") as f:
     received = f.read()
 
 # Bob decrypts the image
 try:
     decrypted = bob.decrypt(received)
 
     with open("decrypted.jpg", "wb") as f:
         f.write(decrypted)
 
     print("Bob: Image decrypted successfully")
     print("Image matches:", image == decrypted)
 
 except InvalidToken:
     print("Security Alert: Invalid key or modified image")
