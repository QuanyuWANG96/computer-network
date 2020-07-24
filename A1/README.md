In this assignment, I use ```Python 3```

# server   
To run the server, try command
```./server.sh  [req_code]```
When the server is running , it will print 
```[SERVER_PORT]: <n_port>```
for example, in this case,
```./server.sh 123```
```SERVER_PORT: 4456```


# client
To run the client, try command
```./client [server_ip] [n_port] [req_code] [message]```
for example,
```./client.sh 127.0.0.1 4456 123 'MESSAGE 1'```