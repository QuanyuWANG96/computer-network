from graph import Graph
# from graph import Vertex
import socket
import threading
from threading import Thread
import sys
import struct

lock = threading.Lock()

class Router:
    def __init__(self, nfe_ip, nfe_port, id):
        self.id = id
        self.graph = Graph()
        self.routing_table = {}  # key: neighbour , value : {key: next_hop, cost, value: neighbour, cost}
        self.cache = set()  # [router_id, router_link_id, router_link_cost]
        self.rcv_info = set()  # [routerID, routerLinkID, routerLinkCost]
        self.links = {}  # key : linkID, value : linkCost

        self.graph.add_vertex(self.id)

        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # send init message
        init_data = struct.pack("!i", 1)  # message type, 0x01
        init_data += struct.pack("!i", self.id)  # router ID
        print("Sending init message data to NFE")
        self.udp_socket.sendto(init_data, (nfe_ip, nfe_port))

    def dijkstra(self):
        lock.acquire()
        N = set()
        D = {}

        previous_routing_table = self.routing_table.copy()

        # init routing table
        adj = list(self.graph.get_vertex(self.id).adjacent.items())
        for neighbor, linkID in adj:
            temp = {}
            temp["next"] = neighbor
            vtx_adj = self.graph.get_vertex(neighbor)
            temp["cost"] = vtx_adj.links[linkID]
            self.routing_table[neighbor] = temp

        # print("%%%%%%%%%%%%%init routing table%%%%%%%%%%%%%%%%%%")
        # print(self.routing_table)

        # calculate the shortest path
        # init vertex set and distance
        for i in list(self.graph.get_all_vertex()):
            N.add(self.graph.get_vertex(i))
            D[i] = sys.maxsize

        adj = list(self.graph.get_vertex(self.id).adjacent.items())
        for neighbor, linkID in adj:
            vtx_adj = self.graph.get_vertex(neighbor)
            D[neighbor] = vtx_adj.links[linkID]
        D[self.id] = 0
        N.remove(self.graph.get_vertex(self.id))
        # print("D :"+ str(D))
        # print("N:" + str(N))
        # print("graph : " + str(self.graph))

        while N:
            min_dist = sys.maxsize
            next_vtx = 0
            # find the current min dist
            for v in N:
                if D[v.id] < min_dist:
                    min_dist = D[v.id]
                    next_vtx = v
            if next_vtx == 0:
                break
            N.remove(next_vtx)
            self.routing_table[next_vtx.id]["cost"] = min_dist

            # updata all dist
            next_router = self.graph.get_vertex(next_vtx.id)
            for neighbor in next_router.adjacent.keys():
                if not neighbor in self.routing_table:
                    self.routing_table[neighbor] = {}

                link_id = next_router.adjacent[neighbor]
                dist_to_neighbor = next_router.links[link_id]
                new_dist = D[next_vtx.id] + dist_to_neighbor
                if new_dist < D[neighbor]:
                    self.routing_table[neighbor]["next"] = self.routing_table[next_vtx.id]["next"]
                    D[neighbor] =new_dist

        # updata routing table
        if self.id in self.routing_table.keys():
            self.routing_table.pop(self.id)

        for route in self.routing_table.keys():
            self.routing_table[route]["cost"] = D[route]
            if D[route] >= sys.maxsize:
                del self.routing_table[route]


        # print("D :" + str(D))
        # print("graph : " + str(self.graph))
        # print("routing table: " + str(self.routing_table))

        if self.routing_table != previous_routing_table:
            # write to topology file
            topo_path = 'topology_' + str(self.id) + '.out'
            topo = open(topo_path, 'a')
            for i in list(self.graph.get_all_vertex()):
                adj = list(self.graph.get_vertex(i).adjacent.items())
                for neighbor, linkID in adj:
                    vtx_adj = self.graph.get_vertex(neighbor)
                    cost = vtx_adj.links[linkID]
                    str_line = "router:" + str(self.graph.get_vertex(i).id) + ", router:" + str(
                        neighbor) + ", linkid:" + str(linkID) + ", cost:" + str(cost) + "\n"
                    topo.write(str_line)
            topo.write("\n")
            # print("write file to topo")
            topo.close()

            # wirte to routing table output file
            r_table_path = 'routingtable_' + str(self.id) + '.out'
            r_table = open(r_table_path, 'a')
            for route in list(self.routing_table.keys()):
                str_line = str(route) + ": " + str(self.routing_table[route]["next"]) + ", " + str(
                    self.routing_table[route]["cost"]) + "\n"
                r_table.write(str_line)
            r_table.write("\n")
            # print("write file to routing table")
            r_table.close()

        lock.release()

    def send_init(self, nfe_ip, nfe_port):
        # send init link info to nfe
        for link in self.links.keys():
            data = struct.pack("!i", 3)  # message type, 0x3
            data += struct.pack("!i", self.id)  # sender_id
            data += struct.pack("!i", link) # sender_link_id
            data += struct.pack("!i", self.id)  # router_id
            data += struct.pack("!i", link)  # router_link_id
            data += struct.pack("!i", self.links[link])  # router_link_cost
            self.udp_socket.sendto(data, (nfe_ip, nfe_port))
            print("Sending(E): SID(" + str(self.id) + "), SLID(" + str(link) + "), RID("+ str(self.id) + "), RLID(" + str(link) + "), LC(" + str(self.links[link])+ ")" )

    def send_forwarding(self, nfe_ip, nfe_port):
        # forwarding phase (LSA)
        while True:
            lock.acquire()

            for router_id, router_link_id, router_link_cost in self.rcv_info:
                if (router_id, router_link_id, router_link_cost) not in self.cache:
                    self.cache.add((router_id, router_link_id, router_link_cost))
                    # send the info to nfe
                    for link in self.links.keys():
                        data = struct.pack("!i", 3)  # message type, 0x3
                        data += struct.pack("!i", self.id)  # sender_id
                        data += struct.pack("!i", link)
                        data += struct.pack("!i", router_id)
                        data += struct.pack("!i", router_link_id)
                        data += struct.pack("!i", router_link_cost)
                        self.udp_socket.sendto(data, (nfe_ip, nfe_port))
                        print("Sending(F): SID(" + str(self.id) + "), SLID(" + str(link) + "), RID(" + str(
                            router_id) + "), RLID(" + str(router_link_id) + "), LC(" + str(
                            router_link_cost) + ")")

                    # get info from rcv_info, updata graph

                    for v in self.graph.get_all_vertex():
                        vtx = self.graph.get_vertex(v)
                        if router_link_id in list(vtx.links.keys()) and router_id != vtx.id:
                            self.graph.add_edge(v, router_id, router_link_id)
                            print("add edge from " + str(v) + " to " + str(router_id) + " through link " + str(
                                router_link_id) + "with cost " + str(router_link_cost))
            lock.release()

            # calculate the latest shortest path and updata routing table
            self.dijkstra()


    def receive_init(self):
        # receive the init reply
        init_buffer, address = self.udp_socket.recvfrom(4096)
        # print("begin to receive")
        message_type_buffer = init_buffer[:4]
        message_type = struct.unpack("!i", message_type_buffer)[0]
        # print("reveive the init relpy, message type: " + str(message_type))
        if message_type not in [1, 2, 3, 4]:
            print(
                "UDP message has an unknown message_type (the first four bytes). Message type received: {} ({})".format(
                    message_type, ' '.join('0x{:02x}'.format(byte) for byte in message_type_buffer)))

        if message_type != 4:
            print("The message type is valid but at this init phase, only Init messages are accepted.")

        # get router's link info from init reply
        num_link_buffer = init_buffer[4:8]
        num_link = struct.unpack("!i", num_link_buffer)[0]
        move = 8
        for i in range(num_link):
            linkID_buffer = init_buffer[move : move + 4]
            linkID = struct.unpack("!i", linkID_buffer)[0]
            move = move + 4
            linkCost_buffer = init_buffer[move: move + 4]
            linkCost = struct.unpack("!i", linkCost_buffer)[0]
            move = move + 4

            self.links[linkID] = linkCost
            self.graph.add_vertex_link(self.id,linkID, linkCost)

    def receive_forward(self):
        # forwarding phase
        while True:
            buffer, address = self.udp_socket.recvfrom(4096)
            # print("begin to receive forwarding phase")
            if len(buffer) != (6 * 4):  # 7 fields, 32-bit (4 bytes) each
                print("Virtual Router {} - message length is {} but that doesn't match expected size, ignoring".format(
                    self.id, len(buffer)))
                continue

            data = struct.unpack("!iiiiii", buffer)
            message_type = data[0]
            if message_type != 3:
                print(
                    "Virtual Router {} - message type is {} but that that's not the expected message type, ignoring".format(
                        self.id, message_type))
                continue

            sender_id = data[1]
            sender_link_id = data[2]
            router_id = data[3]
            router_link_id = data[4]
            router_link_cost = data[5]
            print("Received: SID(" + str(sender_id) + "), SLID(" + str(sender_link_id) + "), RID(" + str(
                router_id) + "), RLID(" + str(router_link_id) + "), LC(" + str(
                router_link_cost) + ")" )

            # drop duplicate router info
            if (router_id, router_link_id, router_link_cost) in self.rcv_info:
                print("Droping: SID(" + str(sender_id) + "), SLID(" + str(sender_link_id) + "), RID(" + str(
                    router_id) + "), RLID(" + str(router_link_id) + "), LC(" + str(
                    router_link_cost) + ")")
            else:
                lock.acquire()
                self.rcv_info.add((router_id, router_link_id, router_link_cost))
                lock.release()

            lock.acquire()
            self.graph.add_vertex(sender_id)
            self.graph.add_vertex(router_id)
            self.graph.add_vertex_link(router_id, router_link_id, router_link_cost)
            lock.release()

            if sender_link_id in self.links.keys():
                cost = self.links[sender_link_id]
                lock.acquire()
                self.graph.add_edge(self.id, sender_id, sender_link_id)
                self.graph.add_vertex_link(sender_id,sender_link_id,cost)
                lock.release()

def main():
    if len(sys.argv) != 4:
        sys.stderr.write("Wrong Numbers of Arguments")
        sys.exit(-1)

    nfe_ip = sys.argv[1]
    nfe_port = int(sys.argv[2])
    router_id = int(sys.argv[3])

    router = Router(nfe_ip, nfe_port, router_id)
    router.receive_init()
    router.send_init(nfe_ip,nfe_port)

    sendThread = Thread(target = router.send_forwarding, args= (nfe_ip,nfe_port,))
    rcvThread = Thread(target = router.receive_forward, args=())
    sendThread.start()
    rcvThread.start()

if __name__ == '__main__':
    main()