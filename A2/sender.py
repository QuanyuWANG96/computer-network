import sys
import socket
import threading
import time
from packet import packet
from threading import Thread

WINDOW_SIZE = 10
TIMEOUT = 0.1
SEQ_NUM_MODULO = packet.SEQ_NUM_MODULO
DATA_LENGTH = 500



class Sender:
    def __init__(self, sender_port):
        self.pkt_list = []
        self.seq_num_log = []
        self.ack_log = []

        self.send_base = 0
        self.next_seq_num = 0
        self.NUM_PKT = 0
        # self.rcv_ack_num = -1
        self.STOP_SIGN = False
        self.lock = threading.Lock()
        self.base_time = time.time()
        self.start_time = time.time()
        self.transmission_time = time.time()

        self.rcv_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rcv_udp_socket.bind(('', sender_port))
        self.send_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def file_to_pkt(self, file_name):
        # print("begin to convert all the file into packet-----------")
        data_file = open(file_name, 'r')
        data = data_file.read(DATA_LENGTH)
        while data:
            self.pkt_list.append(packet.create_packet(self.NUM_PKT, data))
            self.NUM_PKT += 1
            data = data_file.read(DATA_LENGTH)

        # print("begin to packet EOT ---------------------")
        eot = packet.create_eot(self.NUM_PKT)
        self.pkt_list.append(eot)
        self.NUM_PKT += 1

        # print("Number of data packets (include EOT) is: " + str(self.NUM_PKT))

    def send(self,emulator_addr, emulator_port):

        # print("begin send now ------------------")
        self.lock.acquire()
        self.base_time = time.time()
        self.lock.release()
        self.start_time = time.time()

        while not self.STOP_SIGN:
            cur_interval = time.time() - self.base_time
            if cur_interval >= TIMEOUT:  # timeout, resend packet from packet
                # print("-----------------time out resend packet ----------------")
                self.lock.acquire()
                self.next_seq_num = self.send_base
                self.base_time = time.time()
                self.lock.release()

            else: # not timeout
                # check if the sliding window is full,
                if (self.next_seq_num < min(self.NUM_PKT, self.send_base + WINDOW_SIZE)):
                    msg = self.pkt_list[self.next_seq_num].get_udp_data()
                    self.send_udp_socket.sendto(msg, (emulator_addr, emulator_port))
                    self.seq_num_log.append(self.pkt_list[self.next_seq_num].seq_num)
                    # print("success to send pck" + str(self.next_seq_num))
                    self.lock.acquire()
                    self.next_seq_num += 1
                    self.lock.release()

    def receive(self):
        # print("begin to reveive -----------------")
        while True:
            rcv_data , address = self.rcv_udp_socket.recvfrom(4096)
            rcv_ack = packet.parse_udp_data(rcv_data)

            if rcv_ack.type == 2: # receiver has received all packet
                # print("receive all packet, end receive ---------------")
                self.transmission_time = time.time() - self.start_time
                self.lock.acquire()
                self.STOP_SIGN = True
                self.lock.release()
                break
            elif rcv_ack.type == 0:
                self.ack_log.append(rcv_ack.seq_num)
                # print("rcv pkt :" + str(rcv_ack.seq_num))

                distance_base_rcv = 0
                base = self.send_base % SEQ_NUM_MODULO
                if base < rcv_ack.seq_num:
                    # [3(base), 4, 5, 6(rcv_ack), 7, 8(next_seq_num), 9 ...]
                    # [31(rcv_ack), 0(base), 1, 2, 3(next_seq_num), 4 ...]
                    distance_base_rcv = rcv_ack.seq_num - base + 1
                elif base > rcv_ack.seq_num:
                    # [30(base), 31, 0, 1, 2(rcv_ack), 3, 4, 5(next_seq_num), 6, ...]
                    # [29(rcv_ack), 30(base), 31, 0, 1, 2(next_seq_num), 3...]
                    distance_base_rcv = rcv_ack.seq_num + SEQ_NUM_MODULO - base + 1

                # update base based on rcv pkt seq num and update timer as well
                if distance_base_rcv < WINDOW_SIZE:
                    # print("move slide window -------from" + str(self.send_base)  +" to  " + str (self.send_base+distance_base_rcv) )
                    self.send_base += distance_base_rcv
                    self.lock.acquire()
                    self.base_time = time.time()
                    self.lock.release()


    def write_file(self):
        # print("close all socket------------------")
        self.send_udp_socket.close()
        self.rcv_udp_socket.close()

        # print("begin to write log files ---------------")
        seq_file = open('seqnum.log', 'w')
        for seq in self.seq_num_log:
            seq_file.write(str(seq) + '\n')
        seq_file.close()

        ack_file = open('ack.log', 'w')
        for log in self.ack_log:
            ack_file.write(str(log) + '\n')
        ack_file.close()

        time_log = open('time.log', 'w')
        time_log.write(str(self.transmission_time) + '\n')
        time_log.close()

def main():
    if len(sys.argv) != 5:
        sys.stderr.write("Wrong number of arguments")
        exit(1)

    emulator_addr = sys.argv[1]
    emulator_port = int(sys.argv[2])
    sender_port = int(sys.argv[3])
    file_name = sys.argv[4]

    sender = Sender(sender_port)
    sender.file_to_pkt(file_name)

    sendThread = Thread(target = sender.send, args=(emulator_addr, emulator_port,))
    rcvThread = Thread(target = sender.receive, args=())
    sendThread.start()
    rcvThread.start()
    sendThread.join()
    rcvThread.join()

    sender.write_file()

    # print("end of program in sender ---------------")
    exit(0)

if __name__ == '__main__':
    main()