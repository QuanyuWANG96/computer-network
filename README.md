# CS656 Computer Network 

Execute Environment:
This program can be run in Linux student environment at University of Waterloo. I implement the OSPF protocol. We are provided with a network forwarding emulator(nfe.py).

Files:
1. vrouter.py
2. graph.py
3. \_\_init__.py
4. vrouter.sh
5. nfe.py (provided by professor)

Execute:
* nfe.py

command parameters: ```<IP>```,```<port>```,```<topo_file_path>```

execute command example: ```python3 ./nfe.py ubuntu1804-004 18888 test.json```
* vrouter.py

command parameters: ```<nfe_IP>``` ,```<nfe_port>```, ```<routerID>```

execute command example: ```./vrouter.sh ubuntu1804-004 18888 1```

Explaination:
* topology_\<routerID>.out --- topology graph database. Every time an LSA triggers an update to the topology database, it will be output to this file.

```router:<routerid>,router:<routerid>,linkid:<linkid>,cost:<cost>```
* routingtable_\<routerID>.out --- Every time the routing table changes, it will be appended to this file.

```<destination ID>:<next hop ID>,<total cost>```
* std output 

(1) Sending(E):SID(<value>),SLID(<value>),RID(<value>),RLID(<value>),LC(<value>)

(2) Sending(F):SID(<value>),SLID(<value>),RID(<value>),RLID(<value>),LC(<value>)

(3) Received:SID(<value>),SLID(<value>),RID(<value>),RLID(<value>),LC(<value>)

(4) Dropping:SID(<value>),SLID(<value>),RID(<value>),RLID(<value>),LC(<value>)
DROPPING means the LSA is going to be dropped

SENDING(F) means the LSA is being forwarded

SENDING(E) means the LSA is being emitted initially

SID means SenderID,

SLID means SenderLinkID

RID means RouterID

RLID means RouterLinkID

LC means LinkCost

