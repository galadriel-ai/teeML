import socket
import sys
import threading
import time
import guess_encoding


def server(local_ip, local_port, remote_cid, remote_port):
    try:
        dock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dock_socket.bind((local_ip, local_port))
        dock_socket.listen(5)

        while True:
            client_socket = dock_socket.accept()[0]

            server_socket = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
            server_socket.connect((remote_cid, remote_port))

            outgoing_thread = threading.Thread(
                target=forward,
                args=(client_socket,
                      server_socket))
            incoming_thread = threading.Thread(
                target=forward,
                args=(server_socket,
                      client_socket))

            outgoing_thread.start()
            incoming_thread.start()
    finally:
        new_thread = threading.Thread(target=server,
                                      args=(local_ip, local_port, remote_cid,
                                            remote_port))
        new_thread.start()

    return


def forward(source, destination):
    text_done = False
    string = ' '
    while string:
        try:
            string = source.recv(1024)
            try:
                if not text_done:
                    encoding = guess_encoding.execute(string)
                    print("raw bytes:", string)
                    text = string.decode('utf-8', errors='ignore')
                    print("encoding:", encoding, "text:", text)
                    text_done = True
            except Exception as encoding_exc:
                print("EncodingException:", encoding_exc)
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
                              args=(local_ip, local_port, remote_cid,
                                    remote_port))
    thread.start()
    print(
        f"starting forwarder on {local_ip}:{local_port} {remote_cid}:{remote_port}"
    )
    while True:
        time.sleep(60)


if __name__ == '__main__':
    main(sys.argv[1:])
