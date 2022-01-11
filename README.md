# Simple Blockchain

This is a simple blockchain developed in Python.

Wallets are created with their own public - private key pair using PyCryptodome module.

Transactions contain digital signatures, so that tampered transactions can be detected. Transactions are signed using private key and verified using public key of a wallet.

Authenticity of the blockchain can be verified using Proof of Work mechanism, where a brute force problem is solved by a node. This problem is hard to solve, but easy to verify. The miner who solves this problem gets a reward of 200 units.

## Basic Features

1. Add transaction: Adds the transaction to open_transactions.
2. Mining pending blocks: Mines transactions in open_transactions and solves PoW problem.
3. Printing existing blocks in the blockchain.
4. Getting balance of a particular wallet: Gets balance of a wallet from all legitimate transactions.
5. Creating a new wallet with a new public-private key pair
6. Loading existing public-private key pair from wallet.txt
7. Saving public-private key pair to wallet.txt
