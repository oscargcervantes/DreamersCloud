from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
import uuid
import os

api_key = uuid.uuid4().hex

class user:
    
    def __init__(self,name,email,username,password,phone=None,role=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.role = role
        self.username = username
        self.password = password
        self.__hash_password(self.password)
        self.uid = str(uuid.uuid4())
        self.key = str(api_key)
        
    def record(self):
        return {
            "name":self.name,
            "email":self.email,
            "phone":self.phone,
            "username":self.username,
            "password":self.password_hash,
            "id":self.uid,
            "role":self.role,
            "api_key":self.key
        }
    
    def name(self):
        return self.name

    def email(self):
        return self.email
    
    def phone(self):
        return self.phone

    #Private method
    def __hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
