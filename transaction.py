class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    # Overriding __repr__() changes behaviour of print()
    def __repr__(self):
        return "Sender: {}, Recipient: {}, Amount: {}".format(
            self.sender, self.recipient, self.amount
        )
