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
                        <source file='/var/lib/libvirt/images/%s'/>
                        <target dev='hda'/>
                    </disk>
                    <interface type='network'>
                    <source network='default'/>
                    </interface>
                    <input type='mouse' bus='ps2'/>
                    <graphics type='vnc' port='5901' listen='127.0.0.1'/>
                </devices>
            </domain>
        '''
        domainName = str(request.POST["dmN"])
        domainMemory = str(int(request.POST["memory"])*1024*1000)
        domainCurrentMemory = domainMemory
        domainVcpu = str(request.POST["vcpu"])
        domainDisk = f'{domainName}.img'
        domainXML = domainTemplateXML % (domainName,domainMemory,domainCurrentMemory,domainVcpu,domainDisk)
        conn = libvirt.open("qemu:///system")
        domain = conn.defineXML(domainXML)
        conn.close()
        return redirect("post_list")
    return render(request,'blog/vm_add.html',{})


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
    conn.close()
    return redirect("post_list")

def stop_vm(request):
    conn = None
    try:
        conn = libvirt.open("qemu:///system")
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
    domain = conn.lookupByName(request.GET["name"])
    print(request.GET["name"])
    print(domain.name())
    domain.shutdown() #shutdown vm
    conn.close()
    return redirect("post_list")


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

