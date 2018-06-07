# define Python user-defined exceptions
class Error(Exception):
   """Base class for other exceptions"""
   pass
   
class HumiditiesError(Exception):
    pass

def set_humidities(humidities):
    if humidities is None:
        raise HumiditiesError('Value required')

try:
    set_humidities(None)
except HumiditiesError as e:
    print 'Humidities error:', e.message
