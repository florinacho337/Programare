import os
import hashlib
import socket
import threading
import time
import sys

MSG_SIZE = 1024
SHA_START = 1004
TIMEOUT = 5.0


def load_config(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        n_broadcasts = int(lines[0])
        nodes = []
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 2:
                nodes.append((parts[0], int(parts[1])))
        return n_broadcasts, nodes
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)


def create_packet(node_index):
    # Byte 0: Node index
    header = bytes([node_index])
    # Bytes 1-1003: Random values
    payload = os.urandom(1003)
    # Bytes 0-1003 for hashing
    data_to_hash = header + payload
    # Bytes 1004-1023: Binary SHA-1 (exactly 20 bytes)
    sha1_binary = hashlib.sha1(data_to_hash).digest()
    return data_to_hash + sha1_binary


def receiver_worker(sock, total_expected, log_file, err_file):
    received_count = 0
    with open(log_file, 'w') as log_f, open(err_file, 'a') as err_f:
        while received_count < total_expected:
            try:
                sock.settimeout(TIMEOUT)
                # "Insist" on reading full size
                data, addr = sock.recvfrom(MSG_SIZE)

                if len(data) != MSG_SIZE:
                    err_f.write(f"Error: Received incomplete packet of {len(data)} bytes\n")
                    err_f.flush()
                    continue

                # Parse packet
                source_index = data[0]
                sent_sha1_bin = data[SHA_START:MSG_SIZE]
                data_to_hash = data[:SHA_START]

                # Calculate local SHA-1
                calc_sha1_bin = hashlib.sha1(data_to_hash).digest()

                status = "OK" if sent_sha1_bin == calc_sha1_bin else "FAIL"

                # Format: STATUS SRC_INDEX SENT_HEX CALC_HEX
                log_line = (f"{status} {source_index} "
                            f"{sent_sha1_bin.hex()} "
                            f"{calc_sha1_bin.hex()}\n")

                log_f.write(log_line)
                log_f.flush()
                received_count += 1

            except socket.timeout:
                # stop after receiving N*M, so we keep waiting
                continue
            except Exception as e:
                err_f.write(f"Receiver Error: {e}\n")
                err_f.flush()


def sender_worker(sock, n_broadcasts, nodes, my_index, err_file):
    # wait 15 seconds after startup
    time.sleep(15)

    with open(err_file, 'a') as err_f:
        for _ in range(n_broadcasts):
            packet = create_packet(my_index)
            for ip, port in nodes:
                try:
                    # UDP sendto usually handles the whole buffer or fails
                    sock.sendto(packet, (ip, port))

                    # pace the sender to prevent overwhelming the OS buffers
                    time.sleep(0.0001)
                except Exception as e:
                    err_f.write(f"Sender Error to {ip}:{port}: {e}\n")
                    err_f.flush()


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 bcastnode.py <config_file> <node_index>")
        sys.exit(1)

    config_path = sys.argv[1]
    my_index = int(sys.argv[2])

    n_broadcasts, nodes = load_config(config_path)
    m_nodes = len(nodes)
    total_to_receive = n_broadcasts * m_nodes

    # Unique log names per node
    log_file = f"node_{my_index}.log"
    err_file = f"node_{my_index}_error.log"

    try:
        my_ip, my_port = nodes[my_index]
    except IndexError:
        print(f"Index {my_index} not in config.")
        sys.exit(1)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((my_ip, my_port))

    # Threads
    rx_thread = threading.Thread(target=receiver_worker,
                                 args=(sock, total_to_receive, log_file, err_file))
    tx_thread = threading.Thread(target=sender_worker,
                                 args=(sock, n_broadcasts, nodes, my_index, err_file))

    rx_thread.start()
    tx_thread.start()

    tx_thread.join()
    rx_thread.join()
    sock.close()

if __name__ == "__main__":
    main()