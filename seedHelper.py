import hashlib as hlib
import sha3
import binascii
# from cryptotools.BTC import PrivateKey, PublicKey
from ecdsa import SigningKey, SECP256k1


class coinHelper:
    def __init__(self, coin='eth', hasher='sha_256'):
        # print(
        #     'initializing coinhelper'
        # )
        self.coin = coin
        self.hasher = hasher
        self.encoder = 'utf-8'  # ISO-8859-1

    def setCoin(self, coin):
        # print(f'set coin to {coin}')
        self.coin = coin

    def getCoin(self):
        return self.coin

    def setHasher(self, hasher):
        # print(f'changing hasher to {hasher}')
        self.hasher = hasher

    def setEncoder(self, encoder):
        self.encoder = encoder

    def getHash(self, text):
        if self.hasher == "sha_256":
            return hlib.sha256(text.encode(self.encoder)).hexdigest()
        if self.hasher == "sha3_256":
            return hlib.sha3_256(text.encode(self.encoder)).hexdigest()
        if self.hasher == "md5":
            return hlib.md5(text.encode(self.encoder)).hexdigest()
        raise ValueError('Invalid hasher or encoder')

    def getAddress(self, private_key, address_type='P2PKH'):
        keccak = sha3.keccak_256()
        private_key = bytes(private_key, "utf-8")
        private_key = binascii.unhexlify(private_key)
        private = SigningKey.from_string(private_key, curve=SECP256k1)
        if self.coin == "eth":
            public = private.get_verifying_key().to_string()
            keccak.update(public)
            address = "0x{}".format(keccak.hexdigest()[24:])
            return address
        elif self.coin == "btc":
            public = private.get_verifying_key().to_string("uncompressed")
            # public = PublicKey.decode(public)
            # P2PKH (1) for legacy, P2SH for new address (3), P2WPKH (bc) for advanced address
            address = public.to_address(address_type)  #
            return address
        return
