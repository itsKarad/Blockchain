# Simple Blockchain

This is a simple blockchain developed in Python.

Wallets are created with new public-private key pairs using PyCryptodome module.

Transactions contain digital signatures, so that tampered transactions can be detected. Transactions are signed using the private key and verified using the public key of a wallet.

New blocks are mined or added to the blockchain when a connected node solves a hard computational problem. I have used proof of work as a consensus algorithm. When a node solves this PoW problem, it receives an incentive reward of 200 units.

This computational problem is difficult to solve, but very easy to verify. Hence, it's really to verify authenticity of the chain at each time.


## Basic Features

1. Add transaction: Adds the transaction to open_transactions.
2. Mining pending blocks: Mines transactions in open_transactions and solves PoW problem.
3. Printing existing blocks in the blockchain.
4. Getting balance of a particular wallet: Gets balance of a wallet from all legitimate transactions.
5. Creating a new wallet with a new public-private key pair
6. Loading existing public-private key pair from wallet.txt
7. Saving public-private key pair to wallet.txt
