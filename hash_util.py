from hashlib import sha256
import json


def find_hash(block):
    """
    Finds hash of a block
    """
    hashable_block = block.__dict__.copy()
    return sha256(json.dumps(hashable_block).encode()).hexdigest()