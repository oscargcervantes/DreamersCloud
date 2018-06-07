from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
import uuid
import os

api_key = uuid.uuid4().hex

class user:
    
    def __init__(self,name,email,username,password,start_date,two_fa=None,two_fa_configured=None,token_secret=None,phone=None,role=None,profile_photo=None,end_date=None,modified_date=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.role = role
        self.username = username
        self.password = password
        self.__hash_password(self.password)
        self.uid = str(uuid.uuid4())
        self.key = str(api_key)
        self.profile_photo = profile_photo
        self.start_date = start_date
        self.end_date = end_date
        self.modified_date = modified_date
        self.two_fa = two_fa
        self.two_fa_configured = two_fa_configured
        self.token_secret = token_secret
        
        
    def record(self):
        return {
            "name":self.name,
            "email":self.email,
            "phone":self.phone,
            "username":self.username,
            "password":self.password_hash,
            "id":self.uid,
            "role":self.role,
            "api_key":self.key,
            "profile_photo":self.profile_photo,
            "start_date":self.start_date,
            "end_date":self.end_date,
            "modified_date":self.modified_date,
            "two_fa":self.two_fa,
            "two_fa_configured":self.two_fa_configured,
            "token_secret":self.token_secret
        }
    
    def name(self):
        return self.name
    
    def username(self):
        return self.username    

    def email(self):
        return self.email
    
    def phone(self):
        return self.phone

    #Private method
    def __hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
