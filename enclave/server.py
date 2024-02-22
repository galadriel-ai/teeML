import socket
import json
import base64

from NsmUtil import NSMUtil


def main():
    print("Starting server...")

    # Initialise NSMUtil
    nsm_util = NSMUtil()

    # Create a vsock socket object
    client_socket = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)

    # Listen for connection from any CID
    cid = socket.VMADDR_CID_ANY

    # The port should match the client running in parent EC2 instance
    client_port = 5000

    # Bind the socket to CID and port
    client_socket.bind((cid, client_port))

    # Listen for connection from client
    client_socket.listen()

    while True:
        client_connection, addr = client_socket.accept()

        # Get command from client
        payload = client_connection.recv(4096)
        request = json.loads(payload.decode())

        if request["action"] == "ping":
            response = json.dumps({
                "ping": "pong"
            })
            client_connection.send(str.encode(response))
        elif request["action"] == "get_attestation_doc":
            # Generate attestation document
            attestation_doc = nsm_util.get_attestation_doc()
            # Base64 encode the attestation doc
            attestation_doc_b64 = base64.b64encode(attestation_doc).decode()
            attestation_doc_response = json.dumps({
                "attestation_doc_b64": attestation_doc_b64
            })
            client_connection.send(str.encode(attestation_doc_response))
        elif request["action"] == "sign_message":
            try:
                message = request["message"]
                signed_message = nsm_util.sign_message(message)
                request = json.dumps({
                    "signed_message": signed_message
                })
                client_connection.send(str.encode(request))
            except Exception as exc:
                client_connection.send(str.encode(json.dumps({
                    "exception": str(exc)
                })))
        else:
            client_connection.send(str.encode(json.dumps({
                "error": "unknown action: " + request["action"]
            })))

        # Close the connection with client
        client_connection.close()


if __name__ == '__main__':
    main()
