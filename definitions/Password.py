from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
                          
def verify_password(password, password_hash):
    return pwd_context.verify(password, password_hash)

def generate_auth_token(username, uid, expiration=600):
    key = username + uid
    s = Serializer(key, expires_in=expiration)
    return s.dumps({'id': uid})
        
def verify_auth_token(username, uid, token):
    key = username + uid
    s = Serializer(key)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return False    # valid token, but expired
    except BadSignature:
        return False    # invalid token
    return True
