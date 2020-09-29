# CS656 Computer Network 

Execute Environment:
This program can be run in Linux student environment at University of Waterloo. I implement the Go-Back-N(GBN) protocol. We are provided with a network emulator Network Emulator (nEmulator). After that, I also measured the impact of packet loss and delay on transmission time. You can find in [link to report](https://github.com/QuanyuWANG96/computer-network/blob/master/A2/cs656Assignment2.pdf)

Files:
1. receiver.py
2. sender.py
3. packet.py (provided by professor)

Execute:
* sender.py

command parameters:

```<host address of the network emulator>```

```<UDP port number used by the emulator to receive data from the sender>```

```<UDP port number used by the sender to receive ACKs from the emulator>```

```<name of the file to be transferred>```
* receiver.py

command parameters:

```<hostname for the network emulator>``` 

```<UDP port number used by the link emulator to receive ACKs from the receiver>```

```<UDP port number used by the receiver to receive data from the emulator>```

```<name of the file into which the received data is written>```
* Run program

Emulator, on host 1, execute command: ```./nEmulator-linux386 <port1> host2 <port2> <port3> host3 <port4> <max_delay> <discard_prob> <verbose-mode>```

Receiver, on host 2,  execute command: ```./receiver.sh host1 <port3> <port2> <output file>```

Sender, on host 3, execute command: ```./sender.sh host1 <port1> <port4> <input file>```

* Run example

```./nEmulator-linux386 12031 ubuntu1804-004.student.cs.uwaterloo.ca 12034 12033 ubuntu1804-008.student.cs.uwaterloo.ca 12032 1 0.2 1```

```./receiver.sh ubuntu1804-002.student.cs.uwaterloo.ca 12033 12034 'destination_file.txt'```

```./sender.sh ubuntu1804-002.student.cs.uwaterloo.ca 12031 12032 'large.txt'```
