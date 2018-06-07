#!/usr/bin/env python2.7

import pprint

from proxmoxer import ProxmoxAPI
proxmox = ProxmoxAPI('25.93.241.89', user='ocervantez@pam', password='elcomandantedelnorte', verify_ssl=False)
proxmox = ProxmoxAPI('25.93.241.89', user='ocervantez@pam', backend='ssh_paramiko', port=200)
                     
#For SSH publick key access
#from proxmoxer import ProxmoxAPI
#proxmox = ProxmoxAPI('proxmox_host', user='proxmox_admin', backend='ssh_paramiko')

for node in proxmox.nodes.get():
    for vm in proxmox.nodes(node['node']).lxc.get():
        print "{0}. {1} => {2}" .format(vm['vmid'], vm['name'], vm['status'])       

for node in proxmox.nodes.get():
    for vm in proxmox.nodes(node['node']).qemu.get():
        print "{0}. {1} => {2}" .format(vm['vmid'], vm['name'], vm['status']) 

p.pprint(proxmox.nodes('DreamersCloud').lxc.get())
p.pprint(proxmox.nodes('DreamersCloud').lxc('100').status.current.get())
proxmox.nodes('DreamersCloud').lxc('100').config.get()

proxmox.nodes('DreamersCloud').lxc('102').vncproxy.post()
proxmox.nodes('DreamersCloud').lxc('102').vncwebsocket.get(vncticket='PVEVNC:58DB0C8A::jvS3jIPDjv7gtvUzA3LWtBMf6LrFSJDPXOPbw1wzI+fMaGtNqlw1LQSk7qpgxEJUq0+PLWi47uGdFOchKgQYZwh1tp5IBxaVfs+dsrCy/++TbMl8v+zpJ8d1VWh1uKQU9QaKlGwJvd9U1UL/RipCSIVJc5z+P02EUMCj4v+Y+VaebGJkdHeUMTAjgnj5b+8hnWOeaP8Zimtja87icK7Q4coNPo84Bm3pD9/Di8E0Y8R5UvrkK4yOVck77RSRyCQdMkiMNQuXJwdZYcV42Z7OfGg1FE+p7vQ4PDLgWPtIHabpjYe5A1Ha8VjyVTAJZ7/+260mi/qQ0Toa6nFZVkb4xQ==', port='5903')

proxmox.nodes('DreamersCloud').lxc('102').snapshot.post(snapname='102-test1')
proxmox.nodes('DreamersCloud').qemu('100').snapshot.post(snapname='100-test1')


#proxmox.nodes(node['node']).openvz.get()
#proxmox.nodes(node['node']).get('openvz')
#proxmox.get('nodes/%s/openvz' % node['node'])
#proxmox.get('nodes', node['node'], 'openvz')

for vm in proxmox.cluster.resources.get(type='vm'):
    print("{0}. {1} => {2}" .format(vm['vmid'], vm['name'], vm['status']))

p.pprint(proxmox.cluster.resources.get(type='vm'))


node = proxmox.nodes('proxmox_node')
#pprint(node.storage('local').content.get())
pprint.pprint(node)

node = proxmox.nodes.proxmox_node()
#pprint(node.storage.local.content.get())
pprint.pprint(node)

pprint.pprint(proxmox.cluster.resources.get(type='node'))
print " "
pprint.pprint(proxmox.cluster.resources.get(type='vm'))
print " "
pprint.pprint(proxmox.cluster.resources.get(type='storage'))
print " "
pprint.pprint(proxmox.cluster.resources.get())
print " "
pprint.pprint(proxmox.access.users.get())
print " "
pprint.pprint(proxmox.nodes.get())
print "LXC"
#pprint.pprint(proxmox.nodes(node['node/proxmox']).lxc.get())

print len(proxmox.nodes.get())

#raw_input("Start")
#pprint.pprint(proxmox.storage('lvm').content.get())

for node in proxmox.nodes.get():
    #raw_input("Printing nodes")
    #pprint.pprint(node)
    #raw_input("Printing nodes")	
    #for nodeatt in proxmox.nodes(node['node']).get():	
        #raw_input("Printing node attributes")
        #pprint.pprint(nodeatt)
        nodeid = node['node']
        for lxcvm in proxmox.nodes(nodeid).lxc.get():
            #raw_input("Printing LXC attr")
            #pprint.pprint(lxcvm)
            vmid=lxcvm['vmid']
            print (proxmox.nodes(nodeid).lxc(vmid).status.current.get())
            raw_input("Printed VM status")
            pprint.pprint (proxmox.nodes(nodeid).lxc(vmid).config.get())
            pprint.pprint (proxmox.nodes(nodeid).lxc(vmid).firewall.get())
            pprint.pprint (proxmox.nodes(nodeid).lxc(vmid).snapshot.get())
            #pprint.pprint (proxmox.nodes(nodeid).lxc(vmid).feature.get())
            #for st in proxmox.nodes(nodeid).lxc(vmid).status.get():
                #raw_input("Printing ....")
                #pprint.pprint(st['subdir'])

#for node in proxmox.nodes.get():
#    raw_input("Printing nodes")
#    pprint.pprint(node)	
#    for ntw in proxmox.nodes(node['node']).network.get():
#        raw_input("Printing Network")
#        pprint.pprint(ntw)
