from proxy_checks import openai_call
from proxy_checks import sui_debug


def main():
    openai_is_success, openai_error = openai_call.execute()
    sui_is_success, sui_error = sui_debug.execute()

    print("\nChecking proxies:")
    print(f"  OpenAI success={openai_is_success}, error={openai_error}")
    print(f"  SUI success={sui_is_success}, error={sui_error}")
    print("\n")


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print("Exception in check proxies:", exc)
