import chardet


def execute(data: bytes):
    result = chardet.detect(data)
    encoding = result['encoding']
    confidence = result['confidence']  # Value between 0 and 1
    return encoding, confidence


def main():
    # Example usage
    data = b'\x16\x03\x01\x02\x00\x01\x00\x01\xfc\x03\x03!8]\xda\xd89\xcc\x0f\xab\xce\x14\x8c[\x95\xddy\x94r<\xe7\xf2\xc5\x06\xd4\xc6\xa0\xe0@vL1\x94 _\x02\x15\x84E\xe9\xdc\xc1\x86>\x7f=\no\x0f\xed\xec\xe4b\x06\x8e2\xdb\xb0\xd2l\x1e\x05\xd1h\x8fe\x00&\x13\x02\x13\x03\x13\x01\x13\x04\xc0,\xc00\xc0+\xc0/\xcc\xa9\xcc\xa8\xc0$\xc0(\xc0#\xc0\'\x00\x9f\x00\x9e\x00k\x00g\x00\xff\x01\x00\x01\x8d\x00\x00\x00\x13\x00\x11\x00\x00\x0eapi.openai.com\x00\x0b\x00\x04\x03\x00\x01\x02\x00\n\x00\x16\x00\x14\x00\x1d\x00\x17\x00\x1e\x00\x19\x00\x18\x01\x00\x01\x01\x01\x02\x01\x03\x01\x04\x00\x10\x00\x0b\x00\t\x08http/1.1\x00\x16\x00\x00\x00\x17\x00\x00\x001\x00\x00\x00\r\x00"\x00 \x04\x03\x05\x03\x06\x03\x08\x07\x08\x08\x08\t\x08\n\x08\x0b\x08\x04\x08\x05\x08\x06\x04\x01\x05\x01\x06\x01\x03\x03\x03\x01\x00+\x00\x05\x04\x03\x04\x03\x03\x00-\x00\x02\x01\x01\x003\x00&\x00$\x00\x1d\x00 G\xf8px_;G\x89[k\r\xc5\r.\xb7\nkl\xe3\xcf\x96\xec}A\xa7\xf4\x0b\xb5\\#)!\x00\x15\x00\xd6\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    encoding, confidence = execute(data)
    print(f"Guessed encoding: {encoding} with confidence {confidence}")

    encoded = data.decode(encoding)
    print("encoded:", encoded)
    if "api.openai.com" in encoded:
        print("\nis api.openai.com")
    else:
        print("\nis not api.openai.com")


if __name__ == '__main__':
    main()
