#!/usr/bin/env python3

# BTC Pubkey. (only if there are outgoing transactions.)

import os
import requests

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_public_key(bitcoin_address: str) -> str:
    if not bitcoin_address:
        raise ValueError("Bitcoin address cannot be empty.")

    try:
        response = requests.get(f"https://blockchain.info/q/pubkeyaddr/{bitcoin_address}")
        response.raise_for_status()
        public_key = response.text.strip()
        return public_key
    except requests.exceptions.RequestException as e:
        raise ConnectionError("Failed to connect to the Bitcoin blockchain explorer API.") from e
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError("Public key not found for the given Bitcoin address.")
        else:
            raise requests.exceptions.HTTPError("Failed to retrieve public key from the Bitcoin blockchain explorer.") from e

def main():
    clear_terminal()
    bitcoin_address = input("Bitcoin ADDR: ")
    try:
        public_key = get_public_key(bitcoin_address)
        clear_terminal()
        print(f"\n{bitcoin_address}\n\n{public_key}\n")
    except ValueError as ve:
        clear_terminal()
        print(ve)
    except ConnectionError as ce:
        clear_terminal()
        print(ce)

if __name__ == "__main__":
    main()

