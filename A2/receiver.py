from packet import packet
import socket
import sys

SEQ_NUM_MODULO = packet.SEQ_NUM_MODULO  # 32

class Receiver:

    def __init__(self,  receiver_port):
        self.rcv_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rcv_udp_socket.bind(('', receiver_port))
        self.send_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.data_list = []
        self.arrival_log = []
        self.expected_seq_num = 0


    def receive(self, emulator_addr, emulator_port):
        # print("begin to receive -----------------")
        while True:
            rcv_data, address = self.rcv_udp_socket.recvfrom(1024)
            # print("receive a new packet ------------------")
            rcv_packet = packet.parse_udp_data(rcv_data)
            # print("receive pkt seq_num" + str(rcv_packet.seq_num))

            expected_num = self.expected_seq_num % SEQ_NUM_MODULO
            if rcv_packet.seq_num == expected_num:
                if rcv_packet.type == 2:
                    # print("receive all data and begin to send EOT -----------------------")
                    msg = packet.create_eot(rcv_packet.seq_num).get_udp_data()
                    self.send_udp_socket.sendto(msg, (emulator_addr, emulator_port))
                    self.send_udp_socket.close()
                    self.rcv_udp_socket.close()
                    break

                elif rcv_packet.type == 1:
                    self.expected_seq_num += 1
                    self.data_list.append(rcv_packet.data)

            self.arrival_log.append(rcv_packet.seq_num)

            if self.expected_seq_num != 0 :
                # print("begin to send ACK ------------------")
                cur_ack_num = (self.expected_seq_num - 1) % SEQ_NUM_MODULO
                # print("send ack" + str(cur_ack_num))
                ack_msg = packet.create_ack(cur_ack_num).get_udp_data()
                self.send_udp_socket.sendto(ack_msg, (emulator_addr, emulator_port))


    def write_file(self, file_name):
        # print("begin to write arrival log file ----------------------")
        log_file = open('arrival.log', 'w')
        for log in self.arrival_log:
            log_file.write(str(log) + '\n')
        log_file.close()

        # print("begin to write data file ----------------------")
        file = open(file_name, 'w')
        for data in self.data_list:
            file.write(data)
        file.close()

def main():
    if len(sys.argv) != 5:
        sys.stderr.write("Wrong number of arguments")
        exit(1)

    emulator_addr = sys.argv[1]
    emulator_port = int(sys.argv[2])
    receiver_port = int(sys.argv[3])
    file_name = sys.argv[4]

    receiver = Receiver(receiver_port)
    # print("try to receive packet , begin")
    receiver.receive(emulator_addr, emulator_port)
    receiver.write_file(file_name)
    # print("success to write file")

    exit(0)

if __name__ == '__main__':
    main()