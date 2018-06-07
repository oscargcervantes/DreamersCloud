import os, sys
import subprocess
from subprocess import check_output
import shlex
from proxmoxer import ProxmoxAPI
import pprint as p
from Parser import parser

#Call the class as:  
#from Containers import Containers
#Use as:
#c = Containers(100,'debian','LXC','4','test1','1024')
#c.create()

#Call function as from Containers import console
#console(110)

filename = "config.cfg"
ini = parser(filename)
host = ini['proxmox']['host']
user = ini['proxmox']['user']
password = ini['proxmox']['passwd']

try:
    proxmox = ProxmoxAPI(host, user=user, password=password, verify_ssl=False) #Pending to add connection validation and exceptions
except:
	print('Unable to connect to host, ending program')
	sys.exit()

def console(vmid):
        command="pct enter " + str(vmid)
        args = shlex.split(command)
        p = subprocess.call(args)
        return True

def start(vmid):
    print("Starting container")

def stop(vmid):
    print("Stopping container")

#Manage IPs and templates
def get_available_ip():
    print("Available IPs")

def total_container_number():
    cts = proxmox.nodes('DreamersCloud').lxc.get()
    return len(cts)

def list_templates():
    for i in proxmox.nodes('DreamersCloud').storage('local').content.get():
        if i['content'] == 'vztmpl':
            p.pprint(i['volid'])

class Containers:

    def __init__(self, vmid, template_name, description, rootfs_size,hostname,memory,nameserver='8.8.8.8',netname='eth0',netip='10.10.8.100/24',netgw='10.10.8.1',netbridge='vmbr0',storage='local', onboot=1):
        self.vmid = vmid
        self.template_name = template_name
        self.description = description
        self.rootfs_size = rootfs_size
        self.hostname = hostname
        self.memory = memory
        self.nameserver = nameserver
        self.netname = netname
        self.netip = netip
        self.netgw = netgw
        self.netbridge = netbridge
        self.storage = storage
        #self.password = password
        self.onboot = onboot
     
    def getNextVMID(self):
         nextid="pvesh get /cluster/nextid"
         argid = shlex.split(nextid)
         g = subprocess.check_output(argid).decode("utf-8")
         return g.strip()

    #def getNextIP():	         
        
    def create(self):
        #pct create 109 'local:vztmpl/centos-7-default_20160205_amd64.tar.xz' -description LXC -rootfs 4 -hostname pvecontainer01 -memory 1024 -nameserver 8.8.8.8 -net0 name=eth0,ip=10.10.8.2/24,gw=10.10.8.1,bridge=vmbr0 -storage local -password -onboot 1 -unprivileged 1
         new_vmid = self.getNextVMID()
         command="pct create" + " " + new_vmid + " " + str(self.template_name) + " " + "-description" + " "  + str(self.description) + " " + "-rootfs" + " " + str(self.rootfs_size) + " " + "-hostname" + " " + str(self.hostname) + " " + "-memory" + " " + str(self.memory) + " " + "-nameserver" + " " + str(self.nameserver) + " " + "-net0" + " " + "name=" +  str(self.netname) + "," + "ip=" + str(self.netip) + ","  + "gw=" + str(self.netgw) + "," + "bridge=" + str(self.netbridge) + " " + "-storage" + " " + str(self.storage) + " " + "-password"  + " " + "-onboot" + " " + str(self.onboot) 
         #print(command)
         args = shlex.split(command)
         #p = subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
         #output, err = p.communicate() #STDOUT and STDERR
         #ret_value = p.returncode #Return code value ($? on shell)
         h = subprocess.check_output(args).decode("utf-8")
         print(h)
         self.vmid = new_vmid
         #print(ret_value)
        
 
#function to get available ips
#function to start, stop, resume,       
#pct exec 100 command can be passwd to change root password
#Save user, available IPs, etc ..
#IP Management
#User Management
