from time import time


class Block:
    def __init__(self, index, previous_hash, transactions, nonce, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.nonce = nonce
        self.timestamp = time() if timestamp is None else timestamp

    def __repr__(self):
        """
        Overriding __repr__() changes behaviour of print()
        """
        return "Index: {}, Previous hash: {}, Transactions: {} nonce: {}".format(
            self.index, self.previous_hash, self.transactions, self.nonce
        )
