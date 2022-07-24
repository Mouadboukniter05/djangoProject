from pickle import FALSE
from xml import dom
from django.shortcuts import render,redirect
import sys
import os
import libvirt

# Create your views here.
def post_list(request):
    conn = None
    try:
        conn = libvirt.open("qemu:///system")
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
    vcpus = conn.getMaxVcpus("kvm")
    doms = conn.listAllDomains()
    print(doms[0].info())
    nodeinfo = conn.getInfo()
    conn.close()
    return render(request,'blog/post_list.html',{'nodeinfo':nodeinfo,'vcpus':vcpus,'doms':doms})
#-------------------------------------------------------------------------------------------------#
def vm_add(request):
    if request.method=="POST":
        domainTemplateXML='''
            <domain type='kvm'>
                <name>%s</name>
                <memory>%s</memory>
                <currentMemory>%s</currentMemory>
                <vcpu>%s</vcpu>
                <os>
                    <type arch='x86_64' machine='pc'>hvm</type>
                    <boot dev='hd'/>
                </os>
                <devices>
                    <disk type='file' device='disk'>
                        <driver name='qemu' type='qcow2'/>
                        <source file='/home/mouad/images/%s'/>
                        <target dev='hda'/>
                    </disk>
                    <interface type='network'>
                    <source network='default'/>
                    </interface>
                    <input type='mouse' bus='ps2'/>
                    <graphics type='vnc' port='6001' listen='127.0.0.1'/>
                </devices>
            </domain>
        '''
        conn = libvirt.open("qemu:///system")
        domainName = str(request.POST["dmN"])
        exist = conn.lookupByName(domainName)
        print(exist)
        if(exist.name() != ""):
            return render(request,'blog/vm_add.html',{"domain":domainName})
        memo=int(request.POST["memory"])
        domainMemory = str(memo*1000*1024)
        domainCurrentMemory = domainMemory
        domainVcpu = str(request.POST["vcpu"])
        domainDisk = f'{domainName}.qcow'
        os.system(f'qemu-img create -f qcow2 /home/mouad/images/{domainName}.qcow 20G')
        domainXML = domainTemplateXML % (domainName,domainMemory,domainCurrentMemory,domainVcpu,domainDisk)
        domain = conn.defineXML(domainXML)
        conn.close()
         
        return redirect("post_list")
    return render(request,'blog/vm_add.html',{"domain":False})
#-------------------------------------------------------------------------------------------------------------#
def show_vm(request):
    conn = None
    try:
        conn = libvirt.open("qemu:///system")
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
    domain = conn.lookupByName(request.GET["name"])
    print(request.GET["name"])
    os.system(f'virt-viewer {domain.name()}')
    conn.close()
    return redirect("post_list")
#----------------------------------------------------------------------------------------------------------------------#
def docker_vm(request):
    conn = None
    try:
        conn = libvirt.open("qemu:///system")
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
    domain = conn.lookupByName(request.GET["name"])
    print(request.GET["name"])
    conn.close()
    docker=False
    return render(request,'blog/docker_list.html',{'vm':domain,'docker':docker})
#---------------------------------------------------------------------------------------------------------------------#
def details(request):
    conn = None
    try:
        conn = libvirt.open("qemu:///system")
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
    
    vcpus = conn.getMaxVcpus("kvm")
    nodeinfo = conn.getInfo()
    conn.close()
    docker=False
    return render(request,'blog/details.html',{'nodeinfo':nodeinfo,'vcpus':vcpus})
#--------------------------------------------------------------------------------------------------------------------#
def start_vm(request):
    conn = None
    try:
        conn = libvirt.open("qemu:///system")
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
    domain = conn.lookupByName(request.GET["name"])
    print(request.GET["name"])
    print(domain.name())
    domain.create() #start vm
    os.system(f'virt-viewer {domain.name()}')
    conn.close()
    return redirect("post_list")
#---------------------------------------------------------------------------------------------------------------------#
def stop_vm(request):
    conn = None
    try:
        conn = libvirt.open("qemu:///system")
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
    domain = conn.lookupByName(request.GET["name"])
    print(request.GET["name"])
    print(domain.name())
    domain.shutdown()
    while(domain.isActive() != 0):
        pass
    conn.close()
    return redirect("post_list")
#----------------------------------------------------------------------------------------------------------------------#
def destroy_vm(request):
    conn = None
    try:
        conn = libvirt.open("qemu:///system")
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
    domain = conn.lookupByName(request.GET["name"])
    print(request.GET["name"])
    print(domain.name())
    domain.destroy() #destroy vm
    conn.close()
    return redirect("post_list")
#-----------------------------------------------------------------------------------------------------------------------#
def reboot_vm(request):
    conn = None
    try:
        conn = libvirt.open("qemu:///system")
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
    domain = conn.lookupByName(request.GET["name"])
    print(request.GET["name"])
    print(domain.name())
    domain.reboot() #destroy vm
    conn.close()
    return redirect("post_list")

