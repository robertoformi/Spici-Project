import bcrypt

def checkingPassword(inserted_password, rescued_password):
    if bcrypt.checkpw(inserted_password.encode('utf-8'), rescued_password):
        return True
    else:
        return False

def codingPassword(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed