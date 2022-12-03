from chiffrement_payload import charXor, Xor

def payload_possible():
    """
    Ensemble d'arrivée:
    """
    
    ON = []
    OFF = []

    for i in range(0, 1000):
        ON.append("ON " + str(i) )
        OFF.append("OFF " + str(i) )
    ON += OFF 
    return ON

def key_possible():
    """
    Construire une clef contenant pour chaque caractère une liste de lettres possibles.
    """
    car_possible = [ chr(lettre) for lettre in range(ord("A"), ord("Z")+1) ]
    return [car_possible, car_possible, car_possible]



# def findKeyByDico(dico=payload_possible()):
#     key_possible = key_possible()
#     key = ""
#     i = 0
#     for ensemble in key_possible:

#         for lettre in ensemble:
#             if lettre in dico[:][i]:
#                 key += lettre
#                 break
        
#         i+=1
    
#     return key

# def findKeyByDico(payload, dico=payload_possible()):
#     keys = key_possible()
#     keys_possible = [[], [], []]
#     i = 0
#     for ensemble in keys:

#         for lettre in ensemble:

#             print(charXor(lettre, payload[i]))
#             if charXor(lettre, payload[i]) in dico[:,i]:
#                 keys_possible[i].apprend(lettre)
        
#         i+=1
    
#     return keys_possible

def lettre_possible_dico_par_index(dico):
    """
    Pour eviter plusieurs parcours
    """

    i = 0
    max = 0
    possibility = []
    for mot in dico:
        for i in range(len(mot)):
            if i>=max:
                possibility.append([mot[i]])
                max += 1
            elif mot[i] not in possibility[i]:
                possibility[i].append(mot[i])
    
    return possibility
            
#hypothèse: payload valide
def findKeyByDico(payload, dico=payload_possible()):
    dico = lettre_possible_dico_par_index(dico)
    keys = key_possible()
    keys_possible = [[] for i in range(len(keys)) ]
    i = 0
    #On regarde si le xor du payload avec l'une des clés donne quelque chose dans le dico
    for ensemble in keys:
        
        for lettre in ensemble:
            print(charXor(lettre, payload[i]))
            if charXor(lettre, payload[i]) in dico[i]:
                keys_possible[i].append(lettre)
        
        i+=1
    
    return keys_possible

print( findKeyByDico(  Xor("ON 946", "MMA") ) )
#Posibilités trouvées: MEA et MMA
print( Xor( Xor("ON 946", "MMA"),  "MEA") )

#Pour le moment pour connaitre les clés cohrante on test "à la main"
with open("key_possible_a_lire.txt", "w") as f:
    f.write( str(findKeyByDico(  Xor("ON 946", "MMA") )) )


# def adapt_keys(keys):
#     s = []
#     i = 0
#     for ensemble in keys:
#         s.append(ensemble[0])
#         for j in range(1, len(ensemble)):
#                 s.append(keys[0][i] + keys[0][j] + keys[0][k])
#     return s

# #necessité d'adapté pour les chiffres
# def is_coherante(msg):
#     if len(msg) < 6:
#         return False
#     if msg[0:3] == "ON ":
#         return True
#     elif msg[0:3] == "OFF":
#         return True

# def key_coherante(keys, payload):
#     s = []
#     keys = adapt_keys(keys)
#     print(keys)
#     for key in keys:
#         msg = Xor(key, payload)
#         if is_coherante(msg):
#             s.append(msg)
    
#     return s

# print(key_coherante( findKeyByDico(  Xor("ON 946", "MMA") ), "ON 946"))