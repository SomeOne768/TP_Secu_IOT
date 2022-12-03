import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from file_reading import iterFile, test_recovery
import file_reading as f

# # Taking the element for cipher
# key = os.urandom(16)
# iv = os.urandom(16)

# # Choosing the cipher algorithm and the mode
# cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
# encryptor = cipher.encryptor()

# s="nnnffffffffflffddnn".encode("ascii")
# # Takign the cipher text
# ct = encryptor.update(s)
# print(ct)
# # Trying to taking back the real text
# decryptor = cipher.decryptor()
# ct = decryptor.update(ct) + decryptor.finalize()
# print(ct)


def is_valid_test(key, iv, ciphertext, plaintext):
    # AES
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    print(key)
    return None
    ct = encryptor.update(plaintext) + encryptor.finalize()
    
    print(ct)
    print(ciphertext)
    return ct == ciphertext 


def hexato10(hexa):
	if hexa == 'A' or hexa == 'a':
		return 10 
	elif hexa == 'B' or hexa == 'b':
		return 11
	elif hexa == 'C' or hexa == 'c':
		return 12
	elif hexa == 'D' or hexa == 'd':
		return 13 
	elif hexa == 'E' or hexa == 'e':
		return 14 
	elif hexa == 'F' or hexa == 'f':
		return 15

	return int(hexa)

def hextochar(line):
    print(line)
    line = [ int(line[i:i+2], 16) for i in range(0, len(line), 2)]
    print("\n\n\n", line)
    s = ""
    for lettre in line:
        s+= chr( lettre )
    print(s, "\n", s.encode("utf8"))
    return s



for filename in iterFile(f.REPOSITORY1):
    it = iter(f.test_recovery("./aesmct/"+filename))
    
    
    count = next(it)

    key = next(it).encode("utf8")
    # key = bytearray([int(key[i:i+2], 16) for i in range(0, len(key), 2)])

    iv = hextochar(next(it)).encode("utf8")
    # iv = bytearray([int(iv[i:i+2], 16) for i in range(0, len(iv), 2)])
    print(len(iv))
    break 
    
    plaintext = next(it)

    ciphertext = next(it)
    ciphertext = bytearray([int(ciphertext[i:i+2], 16) for i in range(0, len(ciphertext), 2)])

    b = is_valid_test(key, iv, ciphertext, plaintext)
    print(b)
    break
