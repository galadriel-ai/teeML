from eth_account import Account
from web3 import Web3

KEY_PATH = "private_key.txt"

w3 = Web3()


def main():
    account = get_account()
    print(f'account={account.address}')


def get_account():
    key = _get_key()
    if key:
        account = Account.from_key(key)
    else:
        print("no private key, creating new")
        account = w3.eth.account.create()
        _save_key(account)
    return account


def _get_key() -> str:
    try:
        with open(KEY_PATH, "r") as file:
            return file.read()
    except FileNotFoundError:
        return None


def _save_key(account: Account):
    with open(KEY_PATH, "w") as file:
        file.write(w3.to_hex(account.key))


if __name__ == '__main__':
    main()
