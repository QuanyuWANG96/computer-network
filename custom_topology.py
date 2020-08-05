# from mininet.net import Mininet
#
# from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
#
# from mininet.cli import CLI
#
# from mininet.log import setLogLevel
#
# from mininet.link import Link, TCLink
#
#
# def topology():
#     net = Mininet(controller=RemoteController, link=TCLink, switch=OVSKernelSwitch)
#
#     # Add hosts and switches
#
#     Alice = net.addHost('Alice', ip="10.1.1.17/24")
#     Bob = net.addHost('Bob', ip="10.4.4.48/24")
#     Carol = net.addHost('Carol', ip='10.6.6.69/24')
#
#     Robert = net.addHost('Robert')
#     Richard = net.addHost('Richard')
#     Rupert = net.addHost('Rupert')
#
#     s1, s2, s3 = [net.addSwitch(s) for s in 's1', 's2', 's3']
#
#     c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)
#
#     # Alice-eth0 <--> s1-eth1,  Bob-eth0 <--> s2-eth1, Carol-eth0 <--> s3-eth1
#     net.addLink(Alice,s1)
#     net.addLink(Bob, s2)
#     net.addLink(Carol, s3)
#     # for h, s in [ (Alice, s1), (Bob, s2), (Carol, s3) ]:
#     #     net.addLink( h, s )
#
#     net.addLink(Robert, s1)
#     net.addLink(Robert, s2)
#     net.addLink(Richard, s2)
#     net.addLink(Richard, s3)
#     net.addLink(Rupert, s3)
#
#     net.build()
#
#     c0.start()
#
#     s1.start([c0])
#
#     s2.start([c0])
#
#     s3.start([c0])
#
#     Robert.cmd("ifconfig Robert-eth0 0")
#     Robert.cmd("ifconfig Robert-eth1 0")
#     Robert.cmd("ifconfig Robert-eth0 hw ether 00:00:00:00:01:01")
#     Robert.cmd("ifconfig Robert-eth1 hw ether 00:00:00:00:01:02")
#     Robert.cmd("ip route add 10.6.6.0/24 via 10.4.4.46")
#     Robert.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
#
#     Richard.cmd("ifconfig Richard-eth0 0")
#     Richard.cmd("ifconfig Richard-eth1 0")
#     Richard.cmd("ifconfig Richard-eth0 hw ether 00:00:00:00:02:01")
#     Richard.cmd("ifconfig Richard-eth1 hw ether 00:00:00:00:02:02")
#     Richard.cmd("ip route add 10.1.1.0/24 via 10.4.4.14")
#     Richard.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
#
#     Rupert.cmd("ifconfig Rupert-eth0 0")
#     Rupert.cmd("ifconfig Rupert-eth0 hw ether 00:00:00:00:03:01")
#     # Rupert.cmd("ip route add 10.1.1.0/24 via 10.6.6.46 dev Richard-eth1")
#     # Rupert.cmd("ip addr add 10.4.4.0/24 via 10.6.6.46 dev Richard-eth1")
#     Rupert.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
#
#     Carol.cmd("ip route add 10.1.1.0/24 via 10.6.6.46")
#     Carol.cmd("ip route add 10.4.4.0/24 via 10.6.6.46")
#     # Bob.cmd("ip route add 10.1.1.0/24 via 10.4.4.14 dev Bob-eth0")
#     # Bob.cmd("ip addr add 10.1.1.0/24 brd + dev Robert-eth1")
#     Alice.cmd("ip route add 10.6.6.0/24 via 10.1.1.14")
#     Alice.cmd("ip route add 10.4.40/24 via 10.1.1.14")
#
#     s1.cmd("ovs-ofctl add-flow s1 priority=1,arp,actions=flood")
#     s1.cmd("ovs-ofctl add-flow s1 priority=65535,ip,dl_dst=00:00:00:00:01:01,actions=output:2")
#     s1.cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_dst=10.1.1.17/24,actions=output:1")
#
#     s2.cmd("ovs-ofctl add-flow s2 priority=1,arp,actions=flood")
#     s2.cmd("ovs-ofctl add-flow s2 priority=65535,ip,dl_dst=00:00:00:00:01:02,actions=output:2")
#     s2.cmd("ovs-ofctl add-flow s2 priority=65535,ip,dl_dst=00:00:00:00:02:01,actions=output:3")
#     s2.cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_dst=10.6.6.69/24,actions=output:3")
#     s2.cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_dst=10.1.1.17/24,actions=output:2")
#     s2.cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_dst=10.4.4.48/24,actions=output:1")
#
#     s3.cmd("ovs-ofctl add-flow s3 priority=1,arp,actions=flood")
#     s3.cmd("ovs-ofctl add-flow s3 priority=65535,ip,dl_dst=00:00:00:00:02:02,actions=output:2")
#     s3.cmd("ovs-ofctl add-flow s3 priority=10,ip,nw_dst=10.6.6.69/24,actions=output:1")
#
#     print
#     "*** Running CLI"
#
#     CLI(net)
#
#     print
#     "*** Stopping network"
#
#     net.stop()
#
#
# if __name__ == '__main__':
#     setLogLevel('info')
#
#     topology()










from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):
    "A LinuxRouter connecting three IP subnets"

    def build( self, **_opts ):

        Alice = self.addHost('Alice', ip = '10.1.1.17/24')
        Bob = self.addHost('Bob', ip = '10.4.4.48/24')
        Carol = self.addHost('Carol', ip = '10.6.6.69/24')

        s1, s2, s3 = [self.addSwitch(s) for s in 's1', 's2', 's3']

        Robert = self.addNode('Robert', cls=LinuxRouter, ip='10.1.1.14/24')
        Richard = self.addNode('Richard', cls=LinuxRouter, ip='10.4.4.46/24')
        Rupert = self.addNode('Rupert', cls=LinuxRouter, ip='10.6.6.254/24')

        # Alice-eth0 <--> s1-eth1,  Bob-eth0 <--> s2-eth1, Carol-eth0 <--> s3-eth1
        for h, s in [ (Alice, s1), (Bob, s2), (Carol, s3) ]:
            self.addLink( h, s )

        self.addLink(s1, Robert, intfName2='Robert-eth1',
                     params2={'ip' : '10.1.1.14/24'})    # Robert-eth1 <--> s1-eth2
        self.addLink(s2, Robert, intfName2='Robert-eth2',
                     params2={'ip' : '10.4.4.14/24'})    # Robert-eth2 <--> s2-eth2
        self.addLink(s2, Richard, intfName2='Richard-eth1',
                     params2={'ip': '10.4.4.46/24'})     # Richard-eth1 <--> s2-eth3
        self.addLink(s3, Richard, intfName2='Richard-eth2',
                     params2={'ip': '10.6.6.46/24'})     # Richard-eth2 <--> s3-eth2
        self.addLink(s3, Rupert, intfName2='Rupert-eth1',
                     params2={'ip': '10.6.6.254/24'})    # Rupert-eth1 <--> s3-eth3

        # Robert.cmd("ip route add 10.6.6.0/24 via 10.4.4.46")
        # Alice.cmd("ip route add 10.6.6.0/24 via 10.1.1.14")
        # Alice.cmd("ip route add 10.4.4.0/24 via 10.1.1.14")
        # Richard.cmd("ip route add 10.1.1.0/24 via 10.4.4.14")
        # Carol.cmd("ip route add 10.1.1.0/24 via 10.6.6.46")


def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet( topo=topo )
    net.start()
    info( '*** Routing Table on Router:\n' )
    print net[ 'Robert' ].cmd( 'route' )
    print net['Richard'].cmd('route')
    print net['Rupert'].cmd('route')
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()