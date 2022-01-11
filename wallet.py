from Crypto.PublicKey import RSA
from Crypto import Random
import binascii


class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        """
        Saving private & public keys to wallet.txt
        """
        private_key, public_key = self.generate_keys()
        # print("Creating wallet with private_key: {}, public_key: {}".format(private_key, public_key))
        self.private_key = private_key
        self.public_key = public_key

    def load_keys(self):
        """
        Loading private & public keys from wallet.txt
        """
        try:
            with open("wallet.txt") as f:
                keys = f.readlines()
                public_key = keys[0][:-1]
                private_key = keys[1]
                self.public_key = public_key
                self.private_key = private_key
        except:
            print("Loading keys from wallet failed!")

    def save_keys(self):
        try:
            with open("wallet.txt", mode="w") as f:
                f.write(self.public_key)
                f.write("\n")
                f.write(self.private_key)
        except:
            print("Writing to wallet.txt failed!")

    def generate_keys(self):
        """
        Function to generate private-public key pair
        """
        private_rsa_key = RSA.generate(1024, Random.new().read)
        public_rsa_key = private_rsa_key.publickey()
        private_key = binascii.hexlify(private_rsa_key.exportKey(format="DER")).decode(
            "ascii"
        )
        public_key = binascii.hexlify(public_rsa_key.exportKey(format="DER")).decode(
            "ascii"
        )
        return private_key, public_key


if __name__ == "__main__":
    w = Wallet()
    w.load_keys()
