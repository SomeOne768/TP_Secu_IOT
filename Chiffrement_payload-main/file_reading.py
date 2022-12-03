
# Those files contains the name of every 128 aes filename in both directory
REPOSITORY1 = "./aesmct/aesmct_name.txt"
REPOSITORY2 = "./kat_aes/kat_aes_name.txt"

# Step :
# 1 - Open a file with the name of every 128 aes encryption filename
# 2 - for ech file, open it and take every test (group of 5 lines COUNT/Key/Iv/results..)
# 3 - for each group, try to encrypt and then compare with the result expected
# 4 - validate, or not, the algorithms used

# iter on file name


def iterFile(REPOSITORY):
    f = open(REPOSITORY, "r", encoding="utf8")
    for line in f:
        # each line contains filename
        if line[-1] == '\n':
            line = line[:-1]
        yield line

# taking information on a file


def test_recovery(filename):
    f = open(filename, "r", encoding="utf8")
    line = f.readline()
    while line != '':
        
        # Searching for data
        while line.split(" ")[0] != "COUNT" and line != '':
            line = f.readline()

        # checking end of file
        if line != '':
            # The 5 next lines countain data
            COUNT = line.split(" ")[2][:-1]
            line = f.readline()
            KEY = line.split(" ")[2][:-1]
            line = f.readline()
            IV = line.split(" ")[2][:-1]
            line = f.readline()
            PLAINTEXT = line.split(" ")[2][:-1]
            line = f.readline()
            CIPHERTEXT = line.split(" ")[2][:-1]
            yield COUNT
            yield KEY
            yield IV
            yield PLAINTEXT
            yield CIPHERTEXT 

            line = f.readline()