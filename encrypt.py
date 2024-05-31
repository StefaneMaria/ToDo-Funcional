import bcrypt

def encrypt(password):
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash

def checkPassword(hash, password):
    if bcrypt.checkpw(password.encode('utf-8'), hash.encode()):
        return True
    return False