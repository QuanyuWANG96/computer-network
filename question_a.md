# CS656 End of Assessment Part A 


Execute Environment:
This program can be run in Virtual Box with Mininet environment. 
Files:
1. topology.py
2. parta.sh (including all the ovs commands to finish vii problem)

Execute:
execute command: ```sudo python topology.py```

After creating the 10 host and 10 switch topology, open a terminal(xterm) for the switch s2 inside Mininet shell,
execute command: ```xterm s2```

In the xterm terminal for the switch s2, type the command: ```chmod 777 *.sh```, then enter ```./parta.sh```

Come back to the Mininet shell, enter the following commands to check if they are ping successfully.
```h2 ping h4```, ```h4 ping h2```, ```h1 ping h6```, ```h6 ping h1```, ```h0 ping h3```, ```h3 ping h0```. Or you can use ```pingall``` to see all connections.