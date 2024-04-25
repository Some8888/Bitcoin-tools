from typing import Union
import base58
import ecdsa
from bip_utils.utils.crypto.ripemd import Ripemd160
from bip_utils.utils.crypto.sha2 import Sha256
from bip_utils import ElectrumV1, ElectrumV1SeedGenerator, ElectrumV1Languages

BLUE = "\033[94m"
RESET = "\033[0m"

class Hash160:
    @staticmethod
    def QuickDigest(data: Union[bytes, str]) -> bytes:
        return Ripemd160.QuickDigest(Sha256.QuickDigest(data))

mnemonic = input("Mnemonic: ")
seed_bytes = ElectrumV1SeedGenerator(mnemonic, ElectrumV1Languages.ENGLISH).Generate()
electrum_v1 = ElectrumV1.FromSeed(seed_bytes)
private_key_hex = electrum_v1.GetPrivateKey(0, 0).Raw().ToHex()
private_key = bytes.fromhex(private_key_hex)
signing_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
verifying_key = signing_key.get_verifying_key()
public_key_compressed = verifying_key.to_string("compressed")
public_key_uncompressed = verifying_key.to_string("uncompressed")

hash_sha256_step2_compressed = Hash160.QuickDigest(public_key_compressed)
version_byte = b'\x00'
hash_with_version_compressed = version_byte + hash_sha256_step2_compressed
hash_sha256_step5_compressed = Hash160.QuickDigest(hash_with_version_compressed)
checksum_compressed = hash_sha256_step5_compressed[:4]
address_hex_compressed = hash_with_version_compressed + checksum_compressed
bitcoin_address_compressed = base58.b58encode(address_hex_compressed).decode()

hash_sha256_step2_uncompressed = Hash160.QuickDigest(public_key_uncompressed)
hash_with_version_uncompressed = version_byte + hash_sha256_step2_uncompressed
hash_sha256_step5_uncompressed = Hash160.QuickDigest(hash_with_version_uncompressed)
checksum_uncompressed = hash_sha256_step5_uncompressed[:4]
address_hex_uncompressed = hash_with_version_uncompressed + checksum_uncompressed
bitcoin_address_uncompressed = base58.b58encode(address_hex_uncompressed).decode()

wif_compressed = base58.b58encode_check(b'\x80' + private_key + b'\x01')
wif_uncompressed = base58.b58encode_check(b'\x80' + private_key)

print("\n")
print(f"    BTC: {bitcoin_address_compressed} {BLUE}Сompressed{RESET}")
print(f"    WIF: {wif_compressed.decode()}")
print("\n")
print(f"    BTC: {bitcoin_address_uncompressed} {BLUE}Uncompressed{RESET}")
print(f"    WIF: {wif_uncompressed.decode()}")
print("\n")
print(f"    HEX: {private_key_hex}")
print("\n")
