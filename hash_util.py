from hashlib import sha256
import json


def find_hash(block):
    """
    Finds hash of a block
    """
    hashable_block = block.__dict__.copy()
    hashable_block["transactions"] = [
        tx.__dict__ for tx in hashable_block["transactions"]
    ]
    return sha256(json.dumps(hashable_block).encode()).hexdigest()
