# Imports
import json
from utils.hash_util import find_hash
from proof_of_work import verify_proof_of_work, proof_of_work
from block import Block
from transaction import Transaction


class Blockchain:
    def __init__(self, host_id):
        self.__blockchain = []
        self.__open_transactions = []
        self.MINER_REWARD = 200
        self.participants = {"miner"}
        self.GENESIS_BLOCK = Block(
            index=0, previous_hash="", transactions=[], nonce="17", timestamp=0
        )
        self.fetch_data()
        self.hosting_node = host_id

    def get_blockchain(self):
        """
        Return private blockchain
        """
        return self.__blockchain[:]

    def get_open_transactions(self):
        """
        Return private open_transactions
        """
        return self.__open_transactions[:]

    def fetch_data(self):
        """
        Fetches data upon start from data.txt file
        """
        try:
            with open("data.txt", mode="r") as f:
                file_content = f.readlines()
                # Remove \n
                recovered_blockchain = json.loads(file_content[0][:-1])
                for block in recovered_blockchain:
                    block_transactions = [
                        Transaction(tx["sender"], tx["recipient"], tx["amount"])
                        for tx in block["transactions"]
                    ]
                    recovered_block = Block(
                        block["index"],
                        block["previous_hash"],
                        block_transactions,
                        block["nonce"],
                        block["timestamp"],
                    )
                    self.__blockchain.append(recovered_block)
                recovered_open_transactions = json.loads(file_content[1])
                self.__open_transactions = [
                    Transaction(tx["sender"], tx["recipient"], tx["amount"])
                    for tx in recovered_open_transactions
                ]
        except:
            # File not found
            self.__blockchain = [self.GENESIS_BLOCK]
            self.__open_transactions = []

    def save_data(self):
        """
        Saves blockchain & open_transactions to a text file
        """
        with open("data.txt", mode="w") as f:
            saveable_blockchain = [block.__dict__.copy() for block in self.__blockchain]
            for block in saveable_blockchain:
                block["transactions"] = [tx.__dict__ for tx in block["transactions"]]
            saveable_open_transactions = [
                tx.__dict__ for tx in self.__open_transactions
            ]
            f.write(json.dumps(saveable_blockchain))
            f.write("\n")
            f.write(json.dumps(saveable_open_transactions))

    def get_last_blockchain_value(self):
        """
        Returns the last value of the current blockchain
        """
        if len(self.__blockchain) < 1:
            return None
        return self.__blockchain[-1]

    def verify_transaction(self, transaction):
        """
        Verifies if transaction is possible with sender's wallet balance
        """
        if self.get_balance(transaction.sender) >= transaction.amount:
            return True
        print("💵❌ Insufficient funds!")
        return False

    def add_transaction(self, sender, recipient, amount=1.0):
        """
        Adds a transaction to open_transactions list
        Arguments:
            sender: address of sender
            recipient: address of recipient
            amount: amount of money to send
        """
        if not self.hosting_node:
            return False
        new_transaction = Transaction(sender, recipient, amount)
        if not self.verify_transaction(new_transaction):
            print("❌ Transaction verification failed")
            return False
        self.participants.add(sender)
        self.participants.add(recipient)
        self.__open_transactions.append(new_transaction)
        self.save_data()
        return True

    def mine_block(self):
        """
        Creates a new block, verifies proof of work, rewards miners and adds the block to the blockchain
        """
        if not self.hosting_node:
            return False
        previous_block_hash = find_hash(self.__blockchain[-1])
        reward_transaction = Transaction(
            sender="MINING",
            recipient="miner",
            amount=self.MINER_REWARD,
        )
        print("Started proof of work")
        proof = proof_of_work(self.__open_transactions, previous_block_hash)
        print("Finished proof of work with proof {}".format(proof))
        open_transactions_copy = self.__open_transactions[:]
        open_transactions_copy.append(reward_transaction)
        new_block = Block(
            index=len(self.__blockchain),
            previous_hash=previous_block_hash,
            transactions=open_transactions_copy,
            nonce=proof,
        )
        self.__blockchain.append(new_block)
        self.__open_transactions = []
        self.save_data()
        return True

    def get_balance(self, participant):
        """
        Gets balance of a participant from existing transactions on the blockchain
        """
        participant_transactions = []
        balance = 0.0
        for block in self.__blockchain:
            for transaction in block.transactions:
                if transaction.recipient == participant:
                    balance += transaction.amount
                    participant_transactions.append(transaction)
                if transaction.sender == participant:
                    balance -= transaction.amount
                    participant_transactions.append(transaction)
        # Not including open transactions in balance of a participant
        for transaction in self.__open_transactions:
            if transaction.recipient == participant:
                balance += transaction.amount
                participant_transactions.append(transaction)
            if transaction.sender == participant:
                balance -= transaction.amount
                participant_transactions.append(transaction)
        return balance

    def verify_chain(self):
        """
        Verifies if the blockchain is still valid by (a) checking previous_hash for each block (b) Verifying PoW for each block
        """
        prev_hash = find_hash(self.GENESIS_BLOCK)
        for block in self.__blockchain:
            if block.index == 0:
                continue
            if block.previous_hash != prev_hash:
                return False
            if verify_proof_of_work(block.transactions, prev_hash, block.nonce):
                return False
            prev_hash = find_hash(block)
        return True
