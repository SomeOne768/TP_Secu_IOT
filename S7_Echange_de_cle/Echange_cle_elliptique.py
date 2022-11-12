from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

"""
# Generate a private key for use in the exchange.
private_key = X25519PrivateKey.generate()

# In a real handshake the peer_public_key will be received from the
# other party. For this example we'll generate another private key and
# get a public key from that. Note that in a DH handshake both peers
# must agree on a common set of parameters.
peer_public_key = X25519PrivateKey.generate().public_key()
shared_key = private_key.exchange(peer_public_key)

# Perform key derivation.
derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data',
).derive(shared_key)

# For the next handshake we MUST generate another private key.
private_key_2 = X25519PrivateKey.generate()
peer_public_key_2 = X25519PrivateKey.generate().public_key()
shared_key_2 = private_key_2.exchange(peer_public_key_2)
derived_key_2 = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data',
).derive(shared_key_2)

"""

# Generate a private key for use in the exchange.
Alice_private_key = X25519PrivateKey.generate()
Bob_private_key = X25519PrivateKey.generate()

# Convert into bytes
Alice_private_bytes = Alice_private_key.private_bytes(encoding=serialization.Encoding.Raw, format=serialization.PrivateFormat.Raw, encryption_algorithm=serialization.NoEncryption())
Bob_private_bytes = Bob_private_key.private_bytes(encoding=serialization.Encoding.Raw, format=serialization.PrivateFormat.Raw, encryption_algorithm=serialization.NoEncryption())

# Generate the public keys
Alice_public_key = Alice_private_key.public_key()
Bob_public_key = Bob_private_key.public_key()

# Convert into bytes
Alice_public_bytes = Alice_public_key.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)
Bob_public_bytes = Bob_public_key.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)

# shared keys
# Must be equals (here we give public_key for each others)
shared_Alice = Alice_private_key.exchange(Bob_public_key)
shared_Bob = Bob_private_key.exchange(Alice_public_key)


print(Alice_private_key)
print(Alice_public_key)


print(Bob_private_key)
print(Bob_public_key)

print(shared_Alice)
print(shared_Bob)

TOPIC_IOT_public_key = "/ISIMA/S7_DH/GROUPE_4/PublicKeyIoT"
TOPIC_Serveur_public_key = "/ISIMA/S7_DH/GROUPE_4/PublicKeyServer"