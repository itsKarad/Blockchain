from hashlib import sha256

MINING_DIFFICULTY = 3


def find_proof_of_work(transactions, prev_hash, nonce):
    """
    Utility function to check if a given nonce solves the PoW problem
    """
    hasheable_transactions = [tx.__dict__ for tx in transactions]
    input_string = (str(hasheable_transactions) + str(prev_hash) + str(nonce)).encode()
    hash = sha256(input_string).hexdigest()
    return hash[0:MINING_DIFFICULTY] == "000"


def verify_proof_of_work(transactions, prev_hash, nonce):
    """
    Verifies whether the PoW solution is correct
    """
    hasheable_transactions = [tx.__dict__ for tx in transactions]
    input_string = (str(hasheable_transactions) + str(prev_hash) + str(nonce)).encode()
    hash = sha256(input_string).hexdigest()
    return hash[0:MINING_DIFFICULTY] == "000"


def proof_of_work(transactions, prev_hash):
    """
    Attempts to solve the PoW problem by brute force
    """
    nonce = 1
    print("⛏ Mining started")
    while not find_proof_of_work(transactions, prev_hash, nonce):
        nonce += 1
    print("⛏Mining ended with nonce " + str(nonce))
    return nonce
