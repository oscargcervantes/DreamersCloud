
class devices:
    
    def __init__(self,username,type_device,hostname,ip,gw,subnetmask,dns1,dns2,start_date,payment='Hourly',end_date=None,modified_date=None,rebooted_date=None):
        self.username = username
        self.type_device = type_device
        self.hostname = hostname
        self.ip = ip
        self.gw = gw
        self.subnetmask = subnetmask
        self.dns1 = dns1
        self.dns2 = dns2
        self.start_date = start_date
        self.end_date = end_date
        self.modified_date = modified_date
        self.rebooted_date = rebooted_date
        self.payment = payment #Monthly, Hourly
        
    def record(self):
        return {
            "username":self.username,
            "type_device":self.type_device,
            "hostname":self.hostname,
            "ip":self.ip,
            "gw":self.gw,
            "subnetmask":self.subnetmask,
            "dns1":self.dns1,
            "dns2":self.dns2,
            "start_date":self.start_date,
            "payment":self.payment,
            "end_date":self.end_date,
            "modified_date":self.modified_date,
            "rebooted_date":self.rebooted_date            
        }
    
    def username(self):
        return self.username
    
    def type_device(self):
        return self.type_device    

    def hostname(self):
        return self.hostname
