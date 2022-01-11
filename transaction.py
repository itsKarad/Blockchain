class Transaction:
    def __init__(self, sender, recipient, amount, sig):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.sig = sig

    # def __repr__(self):
    #     """
    #     Overriding __repr__() changes behaviour of print()
    #     """
    #     return "Sender: {}, Recipient: {}, Amount: {} Signature: {}".format(
    #         self.sender, self.recipient, self.amount, self.sig
    #     )
