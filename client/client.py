import sys
import socket
import json
import argparse

ATTESTATION_OUTPUT = "attestation_doc_b64.txt"

ACTION_GET_ATTESTATION = "get_attestation_doc"
ACTION_SIGN_MESSAGE = "sign_message"


def save_attestation_b64(attestation_b64):
    with open(ATTESTATION_OUTPUT, "w", encoding="utf-8") as file:
        file.write(attestation_b64)


def _action_get_attestation(s):
    s.send(str.encode(json.dumps({
        "action": ACTION_GET_ATTESTATION
    })))

    # receive the plaintext from the server and print it to console
    response = s.recv(65536)
    attestation_b64 = response.decode()
    attestation_b64_dict = json.loads(attestation_b64)
    save_attestation_b64(attestation_b64_dict["attestation_doc_b64"])
    print("saved attestation doc to:", ATTESTATION_OUTPUT)


def _action_sign_message(s, message):
    s.send(str.encode(json.dumps({
        "action": ACTION_SIGN_MESSAGE,
        "message": message
    })))
    # receive the plaintext from the server and print it to console
    response = s.recv(65536)
    print("response:", response)
    signature_b64 = response.decode()
    print("signature_b64:", signature_b64)


def main(cid: str, action: str, message: str = None):
    # Create a vsock socket object
    s = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
    # The port should match the server running in enclave
    port = 5000
    # Connect to the server
    s.connect((cid, port))

    if action == ACTION_GET_ATTESTATION:
        _action_get_attestation(s)
    elif action == ACTION_SIGN_MESSAGE:
        _action_sign_message(s, message)

    # close the connection
    s.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Enclave client.")
    parser.add_argument(
        "--cid",
        type=int,
        required=True,
        help="an EnclaveCID to connect to"
    )
    parser.add_argument(
        '--action',
        type=str,
        default=ACTION_GET_ATTESTATION,
        choices=[ACTION_GET_ATTESTATION, ACTION_SIGN_MESSAGE],
        help="action to run"
    )
    parser.add_argument(
        "--message",
        type=str,
        help="message to sign in the enclave"
    )

    args = parser.parse_args()
    main(args.cid, args.action)
