#!/bin/bash

#ovs-vsctl set bridge s1 protocols=OpenFlow13
#ovs-vsctl set bridge s2 protocols=OpenFlow13
#ovs-vsctl set bridge s3 protocols=OpenFlow13
#
#ovs-ofctl -O OpenFlow13 add-flow s1 in_port=1,actions=output:2
#ovs-ofctl -O OpenFlow13 add-flow s1 in_port=2,actions=output:1
#
##ovs-ofctl -O OpenFlow13 add-flow s3 in_port=3,actions=output=2
#ovs-ofctl -O OpenFlow13 add-flow s3 in_port=1,actions=output=2
##ovs-ofctl -O OpenFlow13 add-flow s3 ip,nw_dst=10.4.4.48/24,actions=mod_nw_dst=10.6.6.46/24,output=2
##ovs-ofctl -O OpenFlow13 add-flow s3 ip,nw_dst=10.4.4.48/24,actions=output=2
#ovs-ofctl -O OpenFlow13 add-flow s3 in_port=2,actions=output=1
#
##ovs-ofctl -O OpenFlow13 add-flow s2 ip,nw_dst=10.4.4.48/24,actions=output=1
##ovs-ofctl -O OpenFlow13 add-flow s2 in_port=1,ip,nw_src=10.4.4.48,nw_dst=10.1.1.17,actions=output=2
#ovs-ofctl -O OpenFlow13 add-flow s2 in_port=3,actions=output=2
#ovs-ofctl -O OpenFlow13 add-flow s2 in_port=2,actions=output=3
##ovs-ofctl -O OpenFlow13 add-flow s2 in_port=1,ip,nw_src=10.4.4.48,nw_dst=10.6.6.69,actions=output=3
##ovs-ofctl -O OpenFlow13 add-flow s2 ip,nw_dst=10.1.1.0/24,actions=mod_nw_dst=10.4.4.14/24,output=2
##ovs-ofctl -O OpenFlow13 add-flow s2 ip,nw_dst=10.6.6.69/24,actions=mod_nw_dst=10.4.4.46/24,output=3


ifconfig Robert-eth1 0
ifconfig Robert-eth2 0
ifconfig Robert-eth1 hw ether 00:00:00:00:01:01
ifconfig Robert-eth2 hw ether 00:00:00:00:01:02
ip addr add 10.1.1.14/24 brd + dev Robert-eth1
ip addr add 10.4.4.14/24 brd + dev Robert-eth2

ifconfig Richard-eth1 0
ifconfig Richard-eth2 0
ifconfig Richard-eth1 hw ether 00:00:00:00:02:01
ifconfig Richard-eth2 hw ether 00:00:00:00:02:02
ip addr add 10.4.4.46/24 brd + dev Richard-eth1
ip addr add 10.6.6.46/24 brd + dev Richard-eth2

ifconfig Rupert-eth1 0
ifconfig Rupert-eth1 hw ether 00:00:00:00:03:01
ip addr add 10.6.6.254/24 brd + dev Rupert-eth1

echo 1 > /proc/sys/net/ipv4/ip_forward

# route traffic via 192.168.2.254 gateway for 192.168.2.0/24 network:
# ip route add 192.168.2.0/24 via 192.168.2.254 dev eth0
ip route add 10.1.1.0/24 via 10.6.6.46 dev eth0
ip route add 10.4.4.0/24 via 10.6.6.46 dev eth0
ip route add 10.1.1.0/24 via 10.4.4.14 dev eth0

ovs-ofctl add-flow s1 priority=1,arp,actions=flood
ovs-ofctl add-flow s1 priority=65535,ip,dl_dst=00:00:00:00:01:01,actions=output:2
ovs-ofctl add-flow s1 priority=10,ip,nw_dst=10.1.1.17/24,actions=output:1

ovs-ofctl add-flow s2 priority=1,arp,actions=flood
ovs-ofctl add-flow s2 priority=65535,ip,dl_dst=00:00:00:00:01:02,actions=output:2
ovs-ofctl add-flow s2 priority=10,ip,nw_dst=10.6.6.69/24,actions=output:3
ovs-ofctl add-flow s2 priority=65535,ip,dl_dst=00:00:00:00:02:01,actions=output:3
ovs-ofctl add-flow s2 priority=10,ip,nw_dst=10.1.1.17/24,actions=output:2

ovs-ofctl add-flow s3 priority=1,arp,actions=flood
ovs-ofctl add-flow s3 priority=65535,ip,dl_dst=00:00:00:00:02:02,actions=output:2
ovs-ofctl add-flow s3 priority=10,ip,nw_dst=10.6.6.69/24,actions=output:1

