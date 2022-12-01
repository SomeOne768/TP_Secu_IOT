import base64 
import cryptography.hazmat.primitives.ciphers.algorithms as algo
import random



def EncodeXor(tabMessage,tabKey):
    """ Chiffrement Ou exclusif."""
    """ tabMessage contient le message sous forme de tableau d'octets"""
    """ tabKey contient la clef sous forme de tableau d'octets"""
    """ Retourne un tableau d'octets."""
    i = 0
    result = []
    for octet in tabMessage:
        result.append(octet^tabKey[i])
        i = (i+1)%len(tabKey)
    
    return bytearray(result)


def DecodeXor(tabMessage,tabKey):
    """ Chiffrement Ou exclusif."""
    """ tabMessage contient le message sous forme de tableau d'octets"""
    """ tabKey contient la clef sous forme de tableau d'octets"""
    """ Retourne un tableau d'octets."""
    # C'est exactement la même chose
    return EncodeXor(tabMessage, tabKey)


def EncodeBase64(tabMessage):
    """ Encode en base 64 le paramètre chaine"""
    """ tabMessage contient le message sous forme de tableau d'octets"""
    """ Retourne un tableau d'octets."""
    return base64.standard_b64encode(tabMessage)

def DecodeBase64(strMessage):
    """ Decode la chaine encodée en base 64"""
    """ strMessage doit être une chaine ASCII elle sera encodée en utf-8"""
    """ retourne un tableau d'octets"""
    return base64.standard_b64decode(strMessage)


allowed_char = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def gen_payloads(n=16):
    # generer 16 payload
    payloads = []
    pair = True
    for i in range(n):
        s = ""

        # Contient ON ou OFF successivement
        if pair:
            s += "ON"
            pair = False
        else: 
            s += "OFF"
            pair = True
        
        # La cohérence temporelle sera basé sur l'ordre => +1 à chaque fois
        # On le complete en 4 char
        coherence_temporelle = ("0000" + str(i))[-4:]
        s += coherence_temporelle

        # On le complete avec un salage de 8 char
        salage = ''.join(random.choices(allowed_char, k=16-len(s)))

        # On l'insert dans notre liste de payloads
        s+= salage
        payloads.append(s)
    
    return payloads


from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes






if __name__ == '__main__' : 
    tabkey = "1234".encode(encoding="ascii")

    # affichage des 16 payloads
    payloads = gen_payloads()

    # on les passe en bytes
    for i in range(len(payloads)):
        payloads[i] = EncodeBase64(payloads[i].encode(encoding="ascii"))
        payloads[i] = EncodeXor(payloads[i], tabkey)
        payloads[i] = DecodeXor(payloads[i], tabkey)
        payloads[i] = DecodeBase64(payloads[i])

    # Maintenant chiffrement aes
    aes_key = "0123456789012345".encode(encoding='ascii')
    iv = "0123456789".encode(encoding='ascii')
    cipher = Cipher(algorithms.AES(EncodeBase64(aes_key)), modes.CBC( EncodeBase64(iv)))
    encryptor = cipher.encryptor()
    ct = encryptor.update(b"a secret message") + encryptor.finalize()
    print(ct)
    decryptor = cipher.decryptor()
    decryptor.update(ct)
    print(DecodeBase64( ct) )
