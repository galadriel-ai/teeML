module secpk256k1::secpk256k1 {

    use sui::ecdsa_k1;
    use sui::event;
    use oracle::oracle;

    struct ValidationEvent has copy, drop {
        verification_result: bool
    }

    public fun validateSignature(msg: vector<u8>, oracle_key_storage: &oracle::PublicKeyStorage, signature: vector<u8>): bool {
        let public_key = oracle::getPublicKey(oracle_key_storage);
        // The last param 1 represents the hash function used is SHA256, the default hash function used when signing in CLI.
        let verify = ecdsa_k1::secp256k1_verify(&signature, &public_key, &msg, 1);
        event::emit(ValidationEvent { verification_result: verify });
        verify
    }
}
