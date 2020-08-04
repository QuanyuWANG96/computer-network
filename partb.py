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


def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet( topo=topo )  # controller is used by s1-s3
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