# Imports
from hashlib import sha256
import json
import pickle
from hash_util import find_hash
from proof_of_work import verify_proof_of_work, proof_of_work
from block import Block
from transaction import Transaction
from time import time

# Initializing empty blockchain
GENESIS_BLOCK = Block(
    index=0, previous_hash="", transactions=[], nonce="17", timestamp=0
)
blockchain = []
open_transactions = []  # Stores unmined & pending transactions
MINER_REWARD = 200  # Miner reward for completing PoW
participants = {"miner"}  # This address gets the reward (for now)


def save_data():
    """
    Saves blockchain & open_transactions to a text file
    """
    with open("data.txt", mode="w") as f:
        saveable_blockchain = [block.__dict__.copy() for block in blockchain]
        for block in saveable_blockchain:
            block["transactions"] = [tx.__dict__ for tx in block["transactions"]]
        saveable_open_transactions = [tx.__dict__ for tx in open_transactions]
        f.write(json.dumps(saveable_blockchain))
        f.write("\n")
        f.write(json.dumps(saveable_open_transactions))


def fetch_data():
    """
    Fetches data upon start from data.txt file
    """
    try:
        with open("data.txt", mode="r") as f:
            file_content = f.readlines()
            global blockchain
            global open_transactions
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
                blockchain.append(recovered_block)
            recovered_open_transactions = json.loads(file_content[1])
            open_transactions = [
                Transaction(tx["sender"], tx["recipient"], tx["amount"])
                for tx in recovered_open_transactions
            ]
    except:
        # File not found
        blockchain = [GENESIS_BLOCK]
        open_transactions = []


def get_last_blockchain_value():
    """
    Returns the last value of the current blockchain
    """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    """
    Verifies if transaction is possible with sender's wallet balance
    """
    if get_balance(transaction.sender) >= transaction.amount:
        return True
    return False


def add_transaction(sender, recipient, amount=1.0):
    """
    Adds a transaction to open_transactions list
    Arguments:
        sender: address of sender
        recipient: address of recipient
        amount: amount of money to send
    """
    new_transaction = Transaction(sender, recipient, amount)
    if not verify_transaction(new_transaction):
        print("Adding transaction to open_transaction failed!")
        return
    participants.add(sender)
    participants.add(recipient)
    open_transactions.append(new_transaction)
    save_data()


def mine_block():
    """
    Creates a new block, verifies proof of work, rewards miners and adds the block to the blockchain
    """
    previous_block_hash = find_hash(blockchain[-1])
    reward_transaction = Transaction(
        sender="MINING",
        recipient="miner",
        amount=MINER_REWARD,
    )
    print("Started proof of work")
    proof = proof_of_work(open_transactions, previous_block_hash)
    print("Finished proof of work with proof {}".format(proof))
    open_transactions_copy = open_transactions[:]
    open_transactions_copy.append(reward_transaction)
    new_block = Block(
        index=len(blockchain),
        previous_hash=previous_block_hash,
        transactions=open_transactions_copy,
        nonce=proof,
    )
    blockchain.append(new_block)
    save_data()


def get_balance(participant):
    """
    Gets balance of a participant from existing transactions on the blockchain
    """
    participant_transactions = []
    balance = 0.0
    for block in blockchain:
        for transaction in block.transactions:
            if transaction.recipient == participant:
                balance += transaction.amount
                participant_transactions.append(transaction)
            if transaction.sender == participant:
                balance -= transaction.amount
                participant_transactions.append(transaction)
    # Not including open transactions in balance of a participant
    return balance


def get_transaction_details():
    """
    Gets user input for sender, recipient and amount for a transaction
    """
    sender = input("Enter sender address: ")
    recipient = input("Enter recipient address: ")
    amount = float(input("Enter transaction amount: "))
    return (sender, recipient, amount)


def get_user_choice():
    """
    Utility function to get user input
    """
    user_input = input("Your choice: ")
    return user_input


def get_participant():
    """
    Utility function to get participant's name
    """
    user_input = input("Enter name of participant: ")
    return user_input


def print_blockchain_elements():
    """
    Outputting all blocks in the blockchain
    """
    for block in blockchain:
        print(block)


def verify_chain():
    """
    Verifies if the blockchain is still valid by (a) checking previous_hash for each block (b) Verifying PoW for each block
    """
    prev_hash = find_hash(GENESIS_BLOCK)
    for block in blockchain:
        if block.index == 0:
            continue
        if block.previous_hash != prev_hash:
            return False
        if verify_proof_of_work(block.transactions, prev_hash, block.nonce):
            return False
        prev_hash = find_hash(block)
    return True


# Loading data
fetch_data()
print(blockchain)
# Main

waiting_for_input = True
print("Please choose")
print("1: Add a new transaction value")
print("2: Mine blocks")
print("3: Output the blockchain blocks")
print("4: Find balance of partipant")
print("5: Get all participants")
print("6: Check validity of transactions")
print("h: Manipulate the chain")
print("q: Quit")
while waiting_for_input:
    print("*" * 40)
    user_choice = get_user_choice()
    if user_choice == "1":
        transaction_details = get_transaction_details()
        add_transaction(
            transaction_details[0], transaction_details[1], transaction_details[2]
        )
        print(open_transactions)
    elif user_choice == "2":
        mine_block()
        open_transactions = []
        save_data()
    elif user_choice == "3":
        print_blockchain_elements()
    elif user_choice == "4":
        participant = get_participant()
        print("Balance of {} is: {:6.3f}".format(participant, get_balance(participant)))
    elif user_choice == "5":
        print(participants)
    elif user_choice == "q":
        waiting_for_input = False
    else:
        print("Input was invalid, please pick a value from the list!")

    if not verify_chain():
        print("Invalid blockchain!")
        waiting_for_input = False


print("Done!")
