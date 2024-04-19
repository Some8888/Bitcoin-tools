#!/usr/bin/env python3

#			(tips)  If this was useful to you.

#                 BTC:	bc1qnqtqyqfu9rntykn299sp3pydr2vn3khwcvd58t
#                ETH:	0x471c21cD1a37994636cc3e588E57ccfF252c9f57
#    (TRC-20)  USDT:	TH4NgnVWR4mqNH5bgC5aq4qQqmnXdh87v3

#			Convert BTC priv keys.
#			HEX > WIF (Compreesed/Uncompressed)

def hex_to_wif(hex_string):
    import hashlib
    import base58
    hex_private_key = hex_string
    wif_private_key_compressed = b"80" + hex_private_key.encode() + b"01"
    wif_private_key_uncompressed = b"80" + hex_private_key.encode()
    first_sha256 = hashlib.sha256()
    first_sha256.update( bytes.fromhex( wif_private_key_compressed.decode() ) )
    second_sha256 = hashlib.sha256()
    second_sha256.update(first_sha256.digest())
    checksum_compressed = second_sha256.hexdigest()[0:8]
    first_sha256 = hashlib.sha256()
    first_sha256.update( bytes.fromhex( wif_private_key_uncompressed.decode() ) )
    second_sha256 = hashlib.sha256()
    second_sha256.update(first_sha256.digest())
    checksum_uncompressed = second_sha256.hexdigest()[0:8]
    payload_compressed = wif_private_key_compressed.decode() + checksum_compressed
    payload_uncompressed = wif_private_key_uncompressed.decode() + checksum_uncompressed
    wif_private_key_compressed = base58.b58encode(bytes.fromhex(payload_compressed))
    wif_private_key_uncompressed = base58.b58encode(bytes.fromhex(payload_uncompressed))
    return (wif_private_key_compressed.decode(), wif_private_key_uncompressed.decode())

with open("hex.txt", "r") as f:
    with open("wif.txt", "w") as g:
        for line in f:
            line = line.strip()
            wif_compressed, wif_uncompressed = hex_to_wif(line)
            g.write(wif_compressed + "\n")
            g.write(wif_uncompressed + "\n")
