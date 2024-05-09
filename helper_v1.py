#!/usr/bin/env python3

# electrum v1 slow recover.
# 1. create mnemonic list file
# 2. python3 script.py <mnemonic list file>

import sys
import time
from tqdm import tqdm
from bip_utils.wif import WifEncoder
from bip_utils.ecc import Secp256k1PrivateKey
from bip_utils.utils.crypto import Sha256
from bip_utils import ElectrumV1, ElectrumV1SeedGenerator, ElectrumV1Languages

RED = "\033[91m"
RESET = "\033[0m"

TARGET_ADDRESS = "your_btc_addr_here"

def find_bitcoin_address_from_mnemonic(mnemonic, target_address):
    seed_bytes = ElectrumV1SeedGenerator(mnemonic, ElectrumV1Languages.ENGLISH).Generate()
    electrum_v1 = ElectrumV1.FromSeed(seed_bytes)
    private_key = Secp256k1PrivateKey.FromBytes(electrum_v1.GetPrivateKey(0, 0).Raw().ToBytes())
    change_idx = 0
    addr_idx = 0
    address = electrum_v1.GetAddress(change_idx, addr_idx)
    wif_key = WifEncoder.Encode(private_key.Raw().ToBytes())
    if address == target_address:
        return address, wif_key, private_key.Raw().ToHex()
    else:
        return None, None, None

def main():
    if len(sys.argv) != 2:
        print("usage: python3 script.py <mnemonic list file>")
        return

    filename = sys.argv[1]

    try:
        with open(filename, "r") as file:
            mnemonics = file.readlines()
    except FileNotFoundError:
        print(f"'{filename}' not found.")
        return

    start_time = time.time()
    total = len(mnemonics)
    processed = 0
    for mnemonic in tqdm(mnemonics, mininterval=1):
        mnemonic = mnemonic.strip()
        address, wif_key, private_key_hex = find_bitcoin_address_from_mnemonic(mnemonic, TARGET_ADDRESS)

        if address:
            print("\r")
            print(f"     {RED}WIF:{RESET} {wif_key}")
            print("\r")
            print(f"     {RED}HEX:{RESET} {private_key_hex}")
            print("\r")
            
            with open("found", "w") as found_file:
                found_file.write(mnemonic)
                
            return

        processed += 1

    if processed == total:
        print("\n")

main()

