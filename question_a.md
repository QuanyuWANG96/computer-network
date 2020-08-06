# CS656 End of Assessment Part A 
* Question 1

When I first time enter ```h0 ping h1```, it will not work. After we enter all the ovs commands for switch s1 and switch s2, both ```h0 ping h1``` and ```h1 ping h0``` can work.

when adding the following flow table entries,

```ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6634 in_port=1,ip,nw_src=10.0.0.2,nw_dst=10.0.1.2,actions=mod_dl_src:0A:00:0A:01:00:02,mod_dl_dst:0A:00:0A:FE:00:02,output=2```

```ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6635 in_port=2,ip,nw_src=10.0.0.2,nw_dst=10.0.1.2,actions=mod_dl_src:0A:00:01:01:00:01,mod_dl_dst:0A:00:01:02:00:00,output=1```

The first command means it will use OpenFlow protocol 1.3, and switch s0 will add a flow. When switch s0 (```tcp:127.0.0.1:6634```) receive a packet from port 1 with source IP address is ```10.0.0.2```(h0) and destination IP address is ```10.0.1.2``` (h1), it will send the packet to port 2 and set the Ethernet source (```0A:00:0A:01:00:02```, s0-eth2) and destination (```0A:00:0A:FE:00:02```, s1-eth2) address, respectively, to  mac. 
The second command means it will use OpenFlow protocol 1.3, and switch s1 will add a flow. When switch s1 (```tcp:127.0.0.1:6635```) receive a packet from port 2 with source IP address is ```10.0.0.2```(h0) and destination IP address is ```10.0.1.2``` (h1), it will send the packet to port 1 and set the Ethernet source (```0A:00:01:01:00:01```, s1-eth1) and destination (```0A:00:01:02:00:00```, h1-eth0) address, respectively, to  mac. Now, h0 can ping h1 successfully. It means h0 can send packets to h1 and h1 can receive them.

when adding the following flow table entries,

```ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6635 in_port=1,ip,nw_src=10.0.1.2,nw_dst=10.0.0.2,actions=mod_dl_src:0A:00:0A:FE:00:02,mod_dl_dst:0A:00:0A:01:00:02,output=2```

```ovs-ofctl -O OpenFlow13 add-flow tcp:127.0.0.1:6634 in_port=2,ip,nw_src=10.0.1.2,nw_dst=10.0.0.2,actions=mod_dl_src:0A:00:00:01:00:01,mod_dl_dst:0A:00:00:02:00:00,output=1```

The first command means it will use OpenFlow protocol 1.3, and switch s1 will add a flow. When switch s0 (```tcp:127.0.0.1:6635```) receive a packet from port 1 with source IP address is ```10.0.1.2``` (h1) and destination IP address is ```10.0.0.2```(h0), it will send the packet to port 2 and set the Ethernet source (```0A:00:0A:FE:00:02```, s1-eth2) and destination (```0A:00:0A:01:00:02```, s0-eth2) address, respectively, to  mac. 
The second command means it will use OpenFlow protocol 1.3, and switch s0 will add a flow. When switch s1 (```tcp:127.0.0.1:6634```) receive a packet from port 2 with source IP address is ```10.0.1.2``` (h1) and destination IP address is ```10.0.0.2```(h0), it will send the packet to port 1 and set the Ethernet source (```0A:00:00:01:00:01```, s0-eth1) and destination (```0A:00:00:02:00:00```, h0-eth0) address, respectively, to  mac. Now, h1 can ping h0 successfully. It means h1 can send packets to h0 and h0 can receive them.




* Question 2

Execute Environment:
This program can be run in Virtual Box with Mininet environment. 

Files:
1. topology.py
2. parta.sh (including all the ovs commands to finish vii problem)

Execute command: ```sudo python topology.py```

After creating the 10 host and 10 switch topology, open a terminal(xterm) for the switch s2 inside Mininet shell,
execute command: ```xterm s2```

In the xterm terminal for the switch s2, type the command: ```chmod 777 *.sh```, then enter ```./parta.sh```

Come back to the Mininet shell, enter the following commands to check if they are ping successfully.
```h2 ping h4```, ```h4 ping h2```, ```h1 ping h6```, ```h6 ping h1```, ```h0 ping h3```, ```h3 ping h0```. Or you can use ```pingall``` to see all connections.