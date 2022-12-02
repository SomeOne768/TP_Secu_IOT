# On importe nos librairies
import base64
import challenge2_python_cheat_sheet_todo as perso
import partie2 as utilitaire
import random


# Test brut force sur XOR
# On crée des messages chiffrés
allowed_char = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
XOR = utilitaire.gen_payloads()
tabkey = "".join(random.choices(allowed_char, k=4))
# tabkey = "mmmm"


# On chiffre nos payloads avec du XOR
for i in range(len(XOR)):
    XOR[i] = perso.toTab(XOR[i])
    XOR[i] = perso.EncodeXor(XOR[i], perso.toTab(tabkey))


# On sait qu'il doivent contenir ON ou OFF
# On Sait egalement que le chiffrement nous donne des caracteres d'un ensemble definie
allowed_char = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
dictionnaire_mot_recherche = ["ON", "OFF"]


# Lors du décodage tous les char devront donc faire partie de cet ensemble
def dechiffrement_valid(msg, ensemble):
    """ Return true if each caractere of msg are in ensemble otherwise false"""
    for c in msg:
        if not (c in ensemble):
            return False
    return True


# Le message doit contenir soit "ON" soit "OFF"
def is_correct(msg, search_words):
    """ return True if the msg contains at least 1 occurence of an element in seach_words"""
    for word in search_words:
        if perso.Contient(word, msg):
            return True
    return False

### Pour cette partie on detient la fonction contient de la todo sheet

# Biblio d'iter
from itertools import product
import time

def brute_force_attack_XOR(msg, keySize=4):
    allowed_char = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    iter_combi = product(allowed_char, repeat=keySize)
    # print("iter créer")
    keyPossible = []
    for it in iter_combi:
        key = ''.join(it)
        # print(key)
        decode = perso.DecodeXor(msg, perso.toTab(key))
        decode = perso.toStr(decode)

        if dechiffrement_valid(decode, allowed_char):

            if is_correct(decode, ["ON", "OFF"]):
                keyPossible.append(key)
                # print(f"msg: {decode}")
    
    return keyPossible

def key_from_index(usefull_char, indice):
    s = ""
    for i in range(len(usefull_char)):
        s += usefull_char[i][ indice[i] ]
    
    return s

def iterateur_perso(usefull_char):
    keySize = len(usefull_char)
    indice = [0 for i in range(keySize)]
    indice_max = [len(usefull_char[i])-1 for i in range(keySize)]
    key = key_from_index(usefull_char, indice)
    yield key
    while indice != indice_max:
        # on incremente
        j = keySize-1
        trouve = False
        while (j>=0) and indice[j] == indice_max[j]:
            j-=1
        indice[j] += 1

        #Si on ne pouvait pas incrementer avant alors il faut mettre à 0
        j += 1
        while (j<keySize):
            indice[j] = 0
            j+=1

        key = key_from_index(usefull_char, indice)
        yield key





def brute_force_attack_XORv2(msg, keySize=4):
    allowed_char = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    usefull_char = []
    # On ejecte toutes les combi impossible
    for i in range(keySize):
        usefull_char.append("")
        for lettre in allowed_char:
            decode = perso.DecodeXor(msg, perso.toTab(lettre))
            decode = perso.toStr(decode)
            
            if decode[i] in allowed_char:
                usefull_char[i] += decode[i]
    
    iter_combi = iterateur_perso(usefull_char)
    # print("iter créer")
    keyPossible = []
    for it in iter_combi:
        key = ''.join(it)
        # print(key)
        decode = perso.DecodeXor(msg, perso.toTab(key))
        decode = perso.toStr(decode)

        if dechiffrement_valid(decode, allowed_char):

            if is_correct(decode, ["ON", "OFF"]):
                keyPossible.append(key)
                # print(f"msg: {decode}")
    
    return keyPossible


def brut_force_AES(msg, keySize = 128):
    # Taille de cle en octet : 
    keySize = int(keySize/8)
    allowed_char = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    # Au cas ou:
    # allowed_char = [chr(i) for i in range(128)]
    # 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ 
    possibilite = [allowed_char for i in range(keySize)]
    iter_possibilite = iterateur_perso(possibilite)
    keyPossible = []
    
    for key in iter_possibilite:
        decode = perso.DecodeAES_ECB(msg, perso.toTab(key))
        decode = perso.toStr(decode)

        if dechiffrement_valid(decode, allowed_char):

            if is_correct(decode, ["ON", "OFF"]):
                keyPossible.append(key)
    
    return keyPossible

def dico_from_file(filename="francais.txt"):
    dico = []
    with open(filename, "r") as f:
        for line in f:
            s = line.strip('\n')
            dico.append(s)
    
    return dico


def dico_from_file_iter(filename="francais.txt"):
    allowed_char = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    with open(filename, "r") as f:
        for line in f:
            s = line.strip('\n')
            if dechiffrement_valid(s, allowed_char) :
                yield s

def dictionnaire_AES(msg, dico=[], filename="francais.txt"):
    allowed_char = """0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ """
    # allowed_char = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz "
    dico = dico_from_file_iter(filename)
    keyPossible=[]

    for key in dico:
        if (len(key) == 16) :
            try:
                decode = perso.DecodeAES_ECB(msg, perso.toTab(key))
                decode = perso.toStr(decode)

                if dechiffrement_valid(decode, allowed_char):
                    if is_correct(decode, ["ON", "OFF"]):
                        keyPossible.append(key)
            except:
                i = 0
    
    return keyPossible

def afficheXor(keyPass, mess) :
    for key in keyPass :
        phrase = perso.DecodeXor(mess, perso.toTab(key))
        print(key, " : ", perso.toStr(phrase))    

def afficheAES(keyPass, mess) :
    for key in keyPass :
        phrase = perso.DecodeAES_ECB(mess, perso.toTab(key))
        print(key, " : ", perso.toStr(phrase))   

def complementaire_inverser_ordre(key):
    return key[::-1]

def complementaire_inverser_min_maj(key):
    s = ""
    for c in key:
        if c >= 'a' and c <= 'z':
            c = 'A' + c - 'a'
        elif c >= 'A' and c <= 'Z':
            c = 'a' + c - 'a'
        s += c 
    
    return s

def complementaire_premiere_maj(key):
    if key[0] >= 'a' and key[0] <= 'z':
        key[0] = 'A' + key[0] - 'a'
    
    return key

def complementaire_langage_hacker(key):
    # A->4, E->3, O->0, T->7,
    key = key.replace('A', '4')
    key = key.replace('E', '3')
    key = key.replace('O', '0')
    key = key.replace('T', '4')

    # key = key.replace('a', '4')
    # key = key.replace('e', '3')
    # key = key.replace('o', '0')
    # key = key.replace('t', '4')

    return key

if __name__ == '__main__':
    # Teston ça
    # allowed_char = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    # tabkey = "".join(random.choices(allowed_char, k=4))
    # print("key a trouver:")
    # print(tabkey)
    # XOR = utilitaire.gen_payloads(1)[0]
    # XOR = perso.EncodeXor(perso.toTab(XOR), perso.toTab(tabkey))
    # print("message a dechifferer")
    # print(perso.toStr(perso.DecodeXor(XOR, perso.toTab(tabkey))))
    # time.sleep(2)
    # temps_avant = time.time()
    # keys = brute_force_attack_XORv2(XOR, keySize=4)
    # temps_apres = time.time()
    # print(tabkey in keys)
    # time.sleep(2)
    # print(keys)
    # print(f"duree: {temps_apres-temps_avant}")
    # time.sleep(2)
    # for key in keys:
    #     print(perso.DecodeXor(XOR, perso.toTab(key)))

    # AES:
    # message = "ON a decoder"
    # key = "0123456789123456"
    # ct = perso.EncodeAES_ECB(message, perso.toTab(key))

    # keyPossible = brut_force_AES(perso.toTab(message))
    # print(keyPossible)

    dico_from_file()