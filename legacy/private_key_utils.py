def get_private_key(filename):
    with open(filename, mode='r') as key:
        return key.readline()
