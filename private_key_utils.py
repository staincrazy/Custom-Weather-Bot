def getPrivateKey(filename):
    with open(filename, mode='r') as key:
        return key.readline()
