module oracle::oracle {

    use sui::event;
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};

    struct PublicKeyStorage has key {
        id: UID,
        public_key: vector<u8>
    }

    struct PublicKeyAddedEvent has copy, drop {
        public_key: vector<u8>
    }

    struct PublicKeyGetEvent has copy, drop {
        public_key: vector<u8>
    }

    fun init(ctx: &mut TxContext) {
        let public_key_storage = PublicKeyStorage {
            id: object::new(ctx),
            public_key: vector[]
        };

        transfer::transfer(public_key_storage, tx_context::sender(ctx))
    }

    public fun addPublicKey(public_key_storage: &mut PublicKeyStorage, public_key: vector<u8>) {
        public_key_storage.public_key = public_key;
        event::emit(PublicKeyAddedEvent { public_key });
    }

    public fun getPublicKey(public_key_storage: &PublicKeyStorage): vector<u8> {
        event::emit(PublicKeyGetEvent { public_key: public_key_storage.public_key });
        public_key_storage.public_key
    }
}

/*
Example usage:

```shell
# add public key, first argument is the public key storage object id, second argument is the public key:
sui client call \
  --package 0xc5d6cc4d054f150362a4be1d2e50d8e6df9ed55b73f6767e702414826fdc60dc \
  --module oracle \
  --function addPublicKey \
  --gas-budget 100000000 \
  --args 0xd3eae32a81e92ba335ef48bbcff83f15c312f6bb0dffca139775d53c2103d12a "0x027f5fc5283d80756a59b00ab26d2ea914f5d3d35deae839af8806e8f042dd0668"

# get public key, first argument is the public key storage object id:
sui client call \
  --package 0xc5d6cc4d054f150362a4be1d2e50d8e6df9ed55b73f6767e702414826fdc60dc \
  --module oracle \
  --function getPublicKey \
  --gas-budget 100000000 \
  --args 0xd3eae32a81e92ba335ef48bbcff83f15c312f6bb0dffca139775d53c2103d12a
```
*/