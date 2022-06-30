import sys
import libvirt

conn = None
try:
    conn = libvirt.open("qemu:///system")
    
except libvirt.libvirtError as e:
    print(repr(e), file=sys.stderr)
    exit(1)

vcpus = conn.getMaxVcpus("kvm")
nodeinfo = conn.getInfo()
conn.close()
print('Host Model: '+nodeinfo[0])
print('Host Memory size: '+str(nodeinfo[1])+'MB')
print('Host Number of CPUs: '+str(nodeinfo[2]))
print('Host Number of possible vCPUs via KVM hypervisor: '+str(vcpus))
print('MHz of CPUs: '+str(nodeinfo[3]))
print('Number of CPU threads per core: '+str(nodeinfo[7]))
