def charXor(a, b):
    """Returns character a xor b"""
    return chr(ord(a) ^ ord(b))

def Xor(data, key):
    """
    data : string to code/decode
    key : string used as key for encryption
    """

    s = ""
    i = 0
    for c in data:
        s += charXor(c, key[i])
        i = (i + 1) % len(key)

    return s

def toCdecl(ch,prefix="char tab"):
    """
    Fonction which helps to get C++ line declaration
    """
    outp=list(ch)
    return prefix+"[{}]".format(len(outp)+1) + r"""="\x"""+(r"\x".join(["{:02x}".format(ord(_)) for _ in outp]))+r"""";"""

if __name__ == '__main__':
    # print (toCdecl(Xor("TRAVAUX PRATIQUES ISIMA","F")))
    # print (toCdecl(Xor("TRAVAUX PRATIQUES ISIMA","5")))
    # print (toCdecl(Xor("TRAVAUX PRATIQUES ISIMA","F5")))
    # print (toCdecl(Xor("TRAVAUX PRATIQUES ISIMA","ZZ2_F5")))
    # print (toCdecl(Xor("ZZ2_F5","F5")))
    
    # print(Xor(Xor("TRAVAUX PRATIQUES ISIMA","F"), "F"))
    # print(Xor(Xor("TRAVAUX PRATIQUES ISIMA","5"), "5"))
    # print(Xor(Xor("TRAVAUX PRATIQUES ISIMA","F5"), "F5"))
    # print(Xor(Xor("TRAVAUX PRATIQUES ISIMA","ZZ2_F5"), "ZZ2_F5"))
    # print(Xor(Xor("ZZ2_F5","F5"), "F5"))
    # print(toCdecl(Xor("AAAAA", "LOTRO")))


    # chiffrer = Xor("monpayload", "macle")
    # cle = Xor("monpayload", chiffrer)
    # # print(f"message chiffré:{chiffrer}, cle:{cle}" )
    # print("message chiffré: \n", chiffrer, "\ncle: ", cle)
    # print(chiffrer)

    # chiffrer = Xor("ON", "macle")
    # cle = Xor("ON", chiffrer)
    # # print(f"message chiffré:{chiffrer}, cle:{cle}" )
    # print("message chiffré: \n", chiffrer, "\ncle: ", cle)
    # print(chiffrer)



    print(Xor(Xor("ON 946","MMA"), "MMA"))