import base64
import sys

import attestation_verifier

ATTESTATION_DOC_B64_PATH = "attestation_doc_b64.txt"


def _read_attestation_doc():
    with open(ATTESTATION_DOC_B64_PATH, "r", encoding="utf-8") as file:
        return file.read()


def get_root_pem():
    with open('root.pem', 'r', encoding="utf-8") as file:
        return file.read()


def main(pcr0: str):
    root_cert_pem = get_root_pem()

    attestation_doc_b64 = _read_attestation_doc()
    attestation_doc = base64.b64decode(attestation_doc_b64)

    try:
        attestation_verifier.verify_attestation_doc(
            attestation_doc=attestation_doc,
            pcrs=[pcr0],
            root_cert_pem=root_cert_pem
        )
        print("Attestation verification succeeded!")
    except Exception as e:
        # Send error response back to enclave
        print("Attestation verification failed!")

    public_key = attestation_verifier.get_public_key(attestation_doc)
    decode_public_key = attestation_verifier.decode_public_key(public_key)
    print("\ndecode_public_key:", decode_public_key)


if __name__ == '__main__':
    # Get PCR0 from command line parameter
    _pcr0 = sys.argv[1]
    main(_pcr0)
