#!/usr/bin/env python3

# Convert mnemonic (12/18/24) to BTC Legacy addr and priv keys.

import os
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes

class Color:
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

def generate_btc_address_from_mnemonic(mnemonic):
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
    bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
    bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)
    bip44_addr_ctx = bip44_chg_ctx.AddressIndex(0)
    public_key = bip44_addr_ctx.PublicKey().ToAddress()
    private_key_wif = bip44_addr_ctx.PrivateKey().ToWif()
    private_key_hex = bip44_addr_ctx.PrivateKey().Raw().ToHex()
    return public_key, private_key_wif, private_key_hex

def main():
    mnemonic = input("Mnemonic: ")
    address, private_key_wif, private_key_hex = generate_btc_address_from_mnemonic(mnemonic)

    os.system('clear')
    print("\n")
    print(Color.YELLOW + "BTC:" + Color.END, address)
    print(Color.RED + "WIF:" + Color.END, private_key_wif)
    print(Color.RED + "HEX:" + Color.END, private_key_hex)
    print("\n")

if __name__ == "__main__":
    main()
input()

