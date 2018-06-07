import re
import netaddr
from netaddr import *
import base64
import onetimepass
import os

def is_valid_hostname(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1] # strip exactly one dot from the right, if present
    #allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    allowed = re.compile("^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

def validate_fqdn(dn):
    if dn.endswith('.'):
        dn = dn[:-1]
    if len(dn) < 1 or len(dn) > 253:
        return False
    ldh_re = re.compile('^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$',
                        re.IGNORECASE)
    return all(ldh_re.match(x) for x in dn.split('.'))

def is_valid_ip(ip):
    try:
        if IPNetwork(ip):
            ip = IPNetwork(ip) #CIDR 10.10.8.2/24
            return True
        else:
            return False
    except netaddr.AddrFormatError:
        print("Format error")
        return False
    except netaddr.AddrConversionError:
        print("Address conversion error")
        return False
    except netaddr.NotRegisteredError:
        print("Not registered")
        return False

def generate_token():
    return base64.b32encode(os.urandom(10)).decode('utf-8')

def validate_token(token,token_secret):
    return onetimepass.valid_totp(token,token_secret)

def is_valid_password(password=None):
    passlength = len(password)
    minimum_characters = 8
    error = 0	
    if re.search(r'\d', password) and re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and not " " in password and passlength > minimum_characters and password[0].isalpha() and len([x for x in password if x.isdigit()]) > 2:
        return True
    else:
        return False

def is_valid_email(addressToVerify=None):
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)

    if match == None:
	    print('Bad Syntax')
	    return False
    else: 
        return True
