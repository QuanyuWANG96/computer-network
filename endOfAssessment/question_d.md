# CS656 End of Assessment Part D (Graduate Student Project)
student name: Quanyu Wang

student ID: 20812011

student username: q426wang

* Question 1 Describe how OpenFlow protocol can be used to place h2 as a middle box for modifying the UDP traffic between h1 and h0.

In this question, we can see the switch s0 has three ports. ```port 1 <--> host h0```, ```port 2 <--> host h1```, ```port 3 <--> host h2```. 
I need to encrypt the packet from h0 to h1 by placing h2 as a middlebox. I assume that h0 only sends packets to h1 and h1 only sends packets to h0. h2 can only receive the packets from h0 and send packets to h1. 
Thus, I can define the open flow rules  below for switch s0 to achieve it.
1. all packets from port 1 (src_IP = h0, dst_IP = h1) will be sent to port 3.
2. all packets from port 2 (src_IP = h1, dst_IP = h0) will be sent to port 1.
3. all packets from port 3 will be sent to port 2. When it sends to port 2, it need to modify the packet's ```src_IP```, ```src_MAC```, ```src_UDP_port``` back to h0, so that when h1 receives this packet, it thinks it comes from h0 directly and do not know about the middlebox h2.

Since h2 is a middlebox for modifying the UDP traffic between h1 and h0, it means, all the packets coming from h0 (```dst_IP``` = h1) will directly send to h2, 
and h2 will perform some network functions for these packets. After that , it will change ```src_IP```, ```src_MAC```, ```src_UDP_port``` back to h0 and send it.

* Question 2 the OpenFlow rules to implement your approach.
1. ```ovs-ofctl add-flow s0 in_port=1,ip,nw_src=10.0.0.100,nw_dst=10.0.0.101,actions=output:3```
2. ```ovs-ofctl add-flow s0 in_port=2,ip,nw_src=10.0.0.101,nw_dst=10.0.0.100,actions=output:1```
3. ```ovs-ofctl add-flow s0 in_port=3,ip,nw_dst=10.0.0.101,actions=mod_nw_src:10.0.0.100,mod_dl_src:10:00:00:00:00:00,mod_tp_src=h0_UDP_port,output=2```

* Question 3 Explain what the network function running in h2 will look like. You can outline the program running in h2 in a pseudo-code.

In this question, for host h2, it will encrypt the received packets (from h0) and then h2 send it to host h1. The switch s0 will modify the packes' ```src_IP```, ```src_MAC```, ```src_UDP_port``` to its orginal address and UDP port, which is ```h0_IP```, ```h0_MAC```, ```h0_UDP_port```. 
The pseudo-code for host h2 is as follows.
```apex
# assume h2 can only receive the packets from h0 and send packets to h1. 
from socket import *

h1_port = h1_UDP_port
h1 = 10.0.0.101

# encrypt UDP packet by Caesar's code method
def caesar_encryption(data):
    perform the caesar encryption method
    return caesar_encrypted_data

def send_rcv():
    sock = socket(AF_INET, SOCK_STREAM)
    
    while True:
        data, addr = sock.recvfrom(4096)
        data = data.decode()
        caesar_encrypted_data = caesar_encryption(data)
        sock.sendto(caesar_encrypted_data.encode(), (h1, h1_port))

if __name__ = "__main__":
    send_rcv()       
```

