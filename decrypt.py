#! /usr/bin/env python3

# Alternative script for decrypting the vault.
#
# The purpose of this is to provide an example of how to decrypt the HTML
# content outside of Web Crypto. This also serves as a fallback decryption
# method if for whatever reason the browser API is not available.
#
# Requires https://cryptography.io/en/latest/ to be installed:
#
# > pip install cryptography
#

# spell-checker: ignore AESGCM

import argparse
import base64
import getpass
import re

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def main():
    parser = argparse.ArgumentParser(
        description='Decryption utility for a HTML vault')
    parser.add_argument(
        'input',
        help='the encrypted HTML file to parse',
        type=argparse.FileType('r', encoding='UTF-8'))

    args = parser.parse_args()
    vault = ''
    with args.input as inputfile:
        input = inputfile.read()
        re_vault = re.compile(r'<div id="vault">(?P<data>[^<]+)</div>')
        match = re_vault.search(input)
        if match:
            vault = match.group('data')

    vault = vault.strip()
    if len(vault) == 0:
        print('Input file does not have encrypted contents')
        return

    password = getpass.getpass(prompt='Vault password: ')

    parts = vault.split(';;')
    if len(parts) != 3:
        print('Invalid vault contents')

    iv, salt, data = parts[0], parts[1], parts[2]

    iv = base64.b64decode(iv, validate=True)
    salt = base64.b64decode(salt, validate=True)
    data = base64.b64decode(data, validate=True)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        iterations=1000000,
    )
    key = password.encode('utf-8')
    key = kdf.derive(key)

    algo = AESGCM(key)
    cleartext = algo.decrypt(iv, data, None)
    cleartext = cleartext.decode('utf-8')

    print()
    print('----------------------------- CONTENT -----------------------------')
    print(cleartext)
    print('-------------------------------------------------------------------')


if __name__ == '__main__':
    main()
