import sys
from bip_utils.wif import WifEncoder
from bip_utils.ecc import Secp256k1PrivateKey
from bip_utils.utils.crypto.sha2 import Sha256
from bip_utils import ElectrumV1, ElectrumV1SeedGenerator, ElectrumV1Languages

RED = "\033[91m"
RESET = "\033[0m"

mnemonic = input("Mnemonic: ")
seed_bytes = ElectrumV1SeedGenerator(mnemonic, ElectrumV1Languages.ENGLISH).Generate()
electrum_v1 = ElectrumV1.FromSeed(seed_bytes)
private_key = Secp256k1PrivateKey.FromBytes(electrum_v1.GetPrivateKey(0, 0).Raw().ToBytes())
private_key_hex = private_key.Raw().ToHex()

change_idx = 0
addr_idx = 0
address = electrum_v1.GetAddress(change_idx, addr_idx)
wif_key = WifEncoder.Encode(private_key.Raw().ToBytes())

print("\r")
print(f"     {RED}BTC:{RESET} {address}")
print("\r")
print(f"     {RED}WIF:{RESET} {wif_key}")
print("\r")
print(f"     {RED}HEX:{RESET} {private_key_hex}")
print("\r")
