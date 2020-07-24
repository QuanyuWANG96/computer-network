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
        # self.vtx = Vertex(id)
        self.graph = Graph()
        self.routing_table = []
        self.cache = []  # [sender_id, sender_link_id, router_id, router_link_id, router_link_cost]
        self.rcv_info = []  # [routerID, routerLinkID, routerLinkCost]
        self.links = {}  # key : linkID, value : linkCost

        self.graph.add_vertex(self.id)

        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.udp_socket.bind((nfe_ip, nfe_port))

        # send init message
        init_data = struct.pack("!i", 1)  # message type, 0x01
        init_data += struct.pack("!i", self.id)  # router ID
        print("Sending init message data to NFE")
        self.udp_socket.sendto(init_data, (nfe_ip, nfe_port))

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
            print("Sending(E): SID(" + str(self.id) + "), SLID(" + str(link) + "), RID("+ str(self.id) + "), RLID(" + str(link) + "), LC(" + str(self.links[link])+ ")" + "\n")

    def send_forwarding(self, nfe_ip, nfe_port):
        # forwarding phase (LSA)
        while True:
            for sender_id, sender_link_id, router_id, router_link_id, router_link_cost in self.cache:
                if [router_id, router_link_id, router_link_cost] not in self.rcv_info:
                    print("it is a new link info and have not received")
                    self.rcv_info.append([router_id, router_link_id, router_link_cost])

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
                            router_link_cost) + ")" + "\n")

                    # get info from rcv_info, updata graph
                    lock.acquire()
                    for v in self.graph.get_all_vertex():
                        vtx = self.graph.get_vertex(v)
                        if router_link_id in vtx.links.keys() and router_id != vtx.id:
                            self.graph.add_edge(v, router_id, router_link_id, router_link_cost)
                            print("add edge from " + str(v) + " to " + str(router_id) + " through link " + str(
                                router_link_id) + "with cost " + str(router_link_cost))
                    lock.release()

                # drop duplicate router info
                else:
                    print("Droping: SID(" + str(sender_id) + "), SLID(" + str(sender_link_id) + "), RID(" + str(
                        router_id) + "), RLID(" + str(router_link_id) + "), LC(" + str(
                        router_link_cost) + ")" + "\n")

                # delete cur router info in cache
                lock.acquire()
                self.cache.clear()
                lock.release()

    def receive_init(self):
        # receive the init reply
        init_buffer, address = self.udp_socket.recvfrom(4096)
        print("begin to receive")
        message_type_buffer = init_buffer[:4]
        message_type = struct.unpack("!i", message_type_buffer)[0]
        print("reveive the init relpy, message type: " + str(message_type))
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
            print("begin to receive forwarding phase")
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
                router_link_cost) + ")" + "\n")

            lock.acquire()
            self.cache.append([sender_id, sender_link_id, router_id, router_link_id, router_link_cost])

            self.graph.add_vertex(sender_id)
            self.graph.add_vertex(router_id)
            self.graph.add_vertex_link(router_id, router_link_id, router_link_cost)
            # vtx = self.graph.get_vertex(router_id)
            # if vtx == None:
            #     print("can not find this vertex in graph, please check the id")
            # vtx.add_link(router_link_id, router_link_cost)
            if sender_link_id in self.links.keys():
                cost = self.links[sender_link_id]
                self.graph.add_edge(self.id, sender_id, sender_link_id, cost)
                self.graph.add_vertex_link(sender_id,sender_link_id,cost)
                # vtx1 = self.graph.get_vertex(sender_id)
                # if vtx1 == None:
                #     print("can not find this vertex in graph, please check the id")
                # vtx1.add_link(sender_link_id, cost)
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




