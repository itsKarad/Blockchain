from time import time
from transaction import Transaction


class Block:
    def __init__(self, index, previous_hash, transactions, nonce, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.nonce = nonce
        self.timestamp = time() if timestamp is None else timestamp

    # Overriding __repr__() changes behaviour of print()
    def __repr__(self):
        return "Index: {}, Previous hash: {}, Transactions: {} nonce: {}".format(
            self.index, self.previous_hash, self.transactions, self.nonce
        )
