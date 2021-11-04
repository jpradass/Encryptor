#!/usr/bin/python3

import getopt, sys, binascii
from cryptography.fernet import Fernet, InvalidToken

version: str = '1.0.0'

key: str = None
oput: str = None
iput: str = None
mode: str = None

def print_usage():
    print("usage: python3 encryptor.py [command] [value]")
    print("")
    print("commands:")
    print("       --create-key, -c: flag to indicate creation a key to encrypt messages")
    print("       --encrypt, -e/--decrypt, -d: flag to indicate whether encrypt o decrypt mode")
    print("       --key, -k: command to pass the key used to encrypt or decrypt")
    print("       --input, -i/--output, -o: files to read/write message encrypted/decrypted")
    print("       --version, -v: show current version of this app")
    print("")
    print("example: python3 encryptor.py --key Pdu7vMjUzBJ8ekxDpcK-Z0K9jm4bTGS6h3vP4Jn5-_A= --input in.txt --output out.txt --encrypt")

def check_args():
    if not key:
        print('missing param "--key"')
        sys.exit(1)
    if not iput:
        print('missing param "--input"')
        sys.exit(1)
    if not oput:
        print('missing param "--output"')
        sys.exit(1)
    if not mode:
        print('missing option "--encrypt/--decrypt"')
        sys.exit(1)

def read_input() -> str:
    return open(iput, 'rb').read()

def encrypt():
    ii = read_input()
    encrypted = Fernet(key.encode('utf-8')).encrypt(ii)

    open(oput, 'wb').write(encrypted)
    print(f'file {oput} encrypted')

def decrypt():
    try:
        ii = read_input()
        decrypted = Fernet(key.encode('utf-8')).decrypt(ii)

        print("[i] Decrypting successfully:", decrypted.decode('utf-8'))
    except InvalidToken:
        print("[!] Invalid token provided")
    except binascii.Error:
        print("[!] Error decoding key")
    except Exception as err:
        print("[!] There was an error: ", err)

if __name__ == '__main__':
    try:
        options, remainder = getopt.getopt(sys.argv[1:], shortopts='v:k:i:o:e:d:c:h', longopts=['version', 'key=', 'input=', 'output=', 'encrypt', 'decrypt', 'create-key', 'help'])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(1)

    for opt, arg in options:
        if opt in ('--version', '-v'):
            print(f'encryptor v{version}')
            sys.exit(0)
        elif opt in ('--help', '-h'):
            print_usage()
            sys.exit(0)
        elif opt in ('--key', '-k'):
            key = arg
        elif opt in ('--output', '-o'):
            oput = arg
        elif opt in ('--input', '-i'):
            iput = arg
        elif opt in ('--create-key', '-c'):
            print(f'this is the key ==> {Fernet.generate_key().decode("utf-8")}')
            print('store it in a safe place')
            sys.exit(0)
        elif opt in ('--encrypt', '-e'):
            mode = 'encrypt'
        elif opt in ('--decrypt', '-d'):
            mode = 'decrypt'

    check_args()

    encrypt() if mode == 'encrypt' else decrypt()