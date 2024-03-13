from typing import Dict

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


def save_dot_env(dot_env: Dict):
    print("\nsave_dot_env:", dot_env)
    with open("/app/.env", "w") as file:
        for key, value in dot_env.items():
            file.write(key + '="' + value + '"\n')


def save_gcp(gcp_creds_json):
    print("\nsave_gcp:", gcp_creds_json)
    with open("/app/sidekik.json", "w") as file:
        file.write(gcp_creds_json)


if __name__ == '__main__':
    main()
