#!/usr/bin/env python
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import Link, TCLink, Intf
from subprocess import Popen, PIPE
from mininet.log import setLogLevel
import time
import os

if'__main__'==__name__:
    os.system('mn -c')
	setLogLevel('info')
	net = Mininet(link=TCLink)
	key = "net.mptcp.mptcp_enabled"
	value = 0
	p = Popen("sysctl -w %s=%s" %(key,value), shell=True, stdout=PIPE, stderr=PIPE)
	stdout, stderr = p.communicate()
	print("stdout=",stdout,"stderr=",stderr)

    # definisi variable untuk bandwidth
    bandwidth1={'bw':1} # bandwidth 1 mbps
	bandwidth2={'bw':0.5} # bandwidth 500kbps

    # definisi variable untuk router dan host
	hA = net.addHost('host_A')
	hB = net.addHost('host_B')
	R1 = net.addHost('R1')
	R2 = net.addHost('R2')
	R3 = net.addHost('R3')
	R4 = net.addHost('R4')

    #koneksi antar device
	net.addLink(hA,R2,cls=TCLink, **bandwidth1) #host_A-eth1 R2-eth0
	net.addLink(hA,R1,cls=TCLink, **bandwidth1) #host_A-eth0 R1-eth0

	net.addLink(hB,R3,cls=TCLink, **bandwidth1) #host_B-eth0 R3-eth0
	net.addLink(hB,R4,cls=TCLink, **bandwidth1) #host_B-eth1 R4-eth0

	net.addLink(R1,R3,cls=TCLink, **bandwidth2) #R1-eth1 R3-eth1
	net.addLink(R1,R4,cls=TCLink, **bandwidth1) #R1-eth2 R4-eth1

	net.addLink(R2,R3,cls=TCLink, **bandwidth1) #R2-eth1 R3-eth2
	net.addLink(R2,R4,cls=TCLink, **bandwidth2) #R2-eth2 R4-eth2

	net.build()

    #konfiguari host 
    hA.cmd("ifconfig hA-eth0 0")
    hA.cmd("ifconfig hA-eth1 0")
    hA.cmd("ifconfig hA-eth0 192.168.42.1 netmask 255.255.255.0")
    hA.cmd("ifconfig hA-eth1 192.168.52.1 netmask 255.255.255.0")

    hB.cmd("ifconfig hA-eth0 0")
    hB.cmd("ifconfig hA-eth1 0")
    hB.cmd("ifconfig hA-eth0 192.168.62.1 netmask 255.255.255.0")
    hB.cmd("ifconfig hA-eth1 192.168.72.1 netmask 255.255.255.0")

    # konfigurasi router
    R1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    R2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    R3.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    R4.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

    R1.cmd("ifconfig R1-eth0 0")
    R1.cmd("ifconfig R1-eth1 0")
    R1.cmd("ifconfig R1-eth2 0")
    R1.cmd("ifconfig R1-eth0 192.168.42.2 netmask 255.255.255.0")
    R1.cmd("ifconfig R1-eth1 192.168.82.1 netmask 255.255.255.0")
    R1.cmd("ifconfig R1-eth2 192.168.102.1 netmask 255.255.255.0")

    R2.cmd("ifconfig R2-eth0 0")
    R2.cmd("ifconfig R2-eth1 0")
    R2.cmd("ifconfig R2-eth2 0")
    R2.cmd("ifconfig R2-eth0 192.168.52.2 netmask 255.255.255.0")
    R2.cmd("ifconfig R2-eth1 192.168.112.1 netmask 255.255.255.0")
    R2.cmd("ifconfig R2-eth2 192.168.92.1 netmask 255.255.255.0")

    R3.cmd("ifconfig R3-eth0 0")
    R3.cmd("ifconfig R3-eth1 0")
    R3.cmd("ifconfig R3-eth2 0")
    R3.cmd("ifconfig R3-eth0 192.168.62.2 netmask 255.255.255.0")
    R3.cmd("ifconfig R3-eth1 192.168.82.2 netmask 255.255.255.0")
    R3.cmd("ifconfig R3-eth2 192.168.112.2 netmask 255.255.255.0")

    R4.cmd("ifconfig R4-eth0 0")
    R4.cmd("ifconfig R4-eth1 0")
    R4.cmd("ifconfig R4-eth2 0")
    R4.cmd("ifconfig R4-eth0 192.168.72.2 netmask 255.255.255.0")
    R4.cmd("ifconfig R4-eth1 192.168.102.2 netmask 255.255.255.0")
    R4.cmd("ifconfig R4-eth2 192.168.92.2 netmask 255.255.255.0")

    CLI(net)
    net.stop()