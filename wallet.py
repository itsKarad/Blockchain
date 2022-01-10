from Crypto.PublicKey import RSA
from Crypto import Random
import binascii


class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        print("Creating wallet with private_key: {}, public_key: {}".format(private_key, public_key))
        self.private_key = private_key
        self.public_key = public_key

    def load_keys(self):
        pass

    def generate_keys(self):
        """
        Function to generate private-public key pair
        """
        private_key = RSA.generate(1024, Random.new().read)
        public_key = private_key.publickey()
        return (private_key.exportKey().decode(), public_key.exportKey().decode())
