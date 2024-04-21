#!/usr/bin/env python3

# Convert old Electrum mnemonic(v1) to addr and priv.

import hashlib
import base58
import ecdsa
from bip_utils import ElectrumV1, ElectrumV1SeedGenerator, ElectrumV1Languages

mnemonic = input("Mnemonic: ")
seed_bytes = ElectrumV1SeedGenerator(mnemonic, ElectrumV1Languages.ENGLISH).Generate()
electrum_v1 = ElectrumV1.FromSeed(seed_bytes)
private_key_hex = electrum_v1.GetPrivateKey(0, 0).Raw().ToHex()
private_key = bytes.fromhex(private_key_hex)
signing_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
verifying_key = signing_key.get_verifying_key()
public_key_compressed = verifying_key.to_string("compressed")
public_key_uncompressed = verifying_key.to_string("uncompressed")
hash_sha256_step2_compressed = hashlib.sha256(public_key_compressed).digest()
hash_ripemd160_step3_compressed = hashlib.new('ripemd160', hash_sha256_step2_compressed).digest()
version_byte = b'\x00'
hash_with_version_compressed = version_byte + hash_ripemd160_step3_compressed
hash_sha256_step5_compressed = hashlib.sha256(hash_with_version_compressed).digest()
hash_sha256_step6_compressed = hashlib.sha256(hash_sha256_step5_compressed).digest()
checksum_compressed = hash_sha256_step6_compressed[:4]
address_hex_compressed = hash_with_version_compressed + checksum_compressed
bitcoin_address_compressed = base58.b58encode(address_hex_compressed).decode()
hash_sha256_step2_uncompressed = hashlib.sha256(public_key_uncompressed).digest()
hash_ripemd160_step3_uncompressed = hashlib.new('ripemd160', hash_sha256_step2_uncompressed).digest()
hash_with_version_uncompressed = version_byte + hash_ripemd160_step3_uncompressed
hash_sha256_step5_uncompressed = hashlib.sha256(hash_with_version_uncompressed).digest()
hash_sha256_step6_uncompressed = hashlib.sha256(hash_sha256_step5_uncompressed).digest()
checksum_uncompressed = hash_sha256_step6_uncompressed[:4]
address_hex_uncompressed = hash_with_version_uncompressed + checksum_uncompressed
bitcoin_address_uncompressed = base58.b58encode(address_hex_uncompressed).decode()

print("\n")
print(f"   Compressd: {bitcoin_address_compressed}")
print(f"Uncompressed: {bitcoin_address_uncompressed}")
print(f"         hex: {private_key_hex}")
print("\n")
