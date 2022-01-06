from hashlib import sha256
import json


def find_hash(block):
    """
    Finds hash of a block
    """
    return sha256(json.dumps(block).encode()).hexdigest()