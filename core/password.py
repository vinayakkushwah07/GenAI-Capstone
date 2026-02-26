import bcrypt

def secure_pwd(raw_password):
    password_bytes = raw_password.encode('utf-8')
    # salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password

def verify_pwd(plain, hash):
    provided_password_bytes = plain.encode('utf-8')

    return bcrypt.checkpw(provided_password_bytes, hash)