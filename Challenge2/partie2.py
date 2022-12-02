import base64 
import random
import challenge2_python_cheat_sheet_todo as perso


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




if __name__ == '__main__' : 
    

    # affichage des 16 payloads
    payloads = gen_payloads()
    print(payloads)

    #Pour le XOR et l'AES
    XOR = payloads.copy()
    tabkey = "1234".encode(encoding="utf-8")
    AES = payloads.copy()
    aes_key = "0123456789012345".encode(encoding='utf-8')


    # on les passe en bytes on encode et decode
    for i in range(len(XOR)):
        # Encodage
        XOR[i] = perso.EncodeBase64(XOR[i].encode(encoding="utf-8"))
        XOR[i] = perso.EncodeXor(XOR[i], tabkey)
        print(XOR[i])

        # Decodage
        XOR[i] = perso.DecodeXor(XOR[i], tabkey)
        XOR[i] = perso.DecodeBase64(XOR[i])
        print(XOR[i])

    # On essaie maintenant avec l'AES
    for i in range(len(XOR)):
        ct = perso.EncodeAES_ECB(AES[i], aes_key)
        print(ct)
        pt = perso.DecodeAES_ECB(ct, aes_key)
        print(pt)
