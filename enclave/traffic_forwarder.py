import socket
import sys
import threading
import time

BUFFER_SIZE = 1024

REMOTE_CID = 3
REMOTE_PORT_OPENAI = 8002
REMOTE_PORT_SUI = 8003


def guess_the_destination_port(data: bytes) -> int:
    # the encoding is not utf-8 nor ascii, so ignoring errors and doing best guess
    text = data.decode('utf-8', errors='ignore')
    print("  text:", text)
    if "api.openai.com" in text:
        return REMOTE_PORT_OPENAI
    elif "fullnode.devnet.sui.io" in text:
        return REMOTE_PORT_SUI
    # TODO: what if no destination?
    return REMOTE_PORT_SUI


def server(local_ip, local_port):
    try:
        dock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dock_socket.bind((local_ip, local_port))
        dock_socket.listen(5)

        while True:
            client_socket = dock_socket.accept()[0]
            first_batch = client_socket.recv(BUFFER_SIZE)
            destination_port = guess_the_destination_port(first_batch)
            print("Got destination port:", destination_port)

            server_socket = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
            server_socket.connect((REMOTE_CID, destination_port))

            outgoing_thread = threading.Thread(
                target=forward,
                args=(client_socket,
                      server_socket, first_batch))
            incoming_thread = threading.Thread(
                target=forward,
                args=(server_socket,
                      client_socket))

            outgoing_thread.start()
            incoming_thread.start()
    finally:
        new_thread = threading.Thread(target=server,
                                      args=(local_ip, local_port))
        new_thread.start()

    return


def forward(source, destination, first_string: bytes = None):
    if first_string:
        destination.sendall(first_string)

    string = ' '
    while string:
        try:
            string = source.recv(BUFFER_SIZE)
            if string:
                destination.sendall(string)
            else:
                source.shutdown(socket.SHUT_RD)
                destination.shutdown(socket.SHUT_WR)
        except Exception as exc:
            print("Exception in forward:", exc)


def main(args):
    local_ip = str(args[0])
    local_port = int(args[1])
    remote_cid = int(args[2])
    remote_port = int(args[3])

    thread = threading.Thread(target=server,
                              args=(local_ip, local_port))
    thread.start()
    print(
        f"starting forwarder on {local_ip}:{local_port} {remote_cid}:{remote_port}"
    )
    while True:
        time.sleep(60)


if __name__ == '__main__':
    main(sys.argv[1:])
