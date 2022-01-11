from block import Block
from blockchain import Blockchain
from uuid import uuid4
from wallet import Wallet


class Node:
    def __init__(self):
        self.node_id = str(uuid4())
        self.wallet = Wallet()
        self.chain = Blockchain(self.wallet.public_key)
        self.listen_for_input()

    def listen_for_input(self):
        """
        Method to listen to user inputs upon starting the program
        """
        waiting_for_input = True
        print("Please choose")
        print("1: Add a new transaction value")
        print("2: Mine blocks")
        print("3: Output the blockchain blocks")
        print("4: Find balance of partipant")
        print("5: Create new wallet")
        print("6: Load existing keys")
        print("7: Save keys")
        print("q: Quit")
        while waiting_for_input:
            print("*" * 40)
            user_choice = self.get_user_choice()
            if user_choice == "1":
                transaction_details = self.get_transaction_details()
                if self.wallet.public_key == None:
                    print("💸❌ Adding transaction failed, Please connect wallet first!")
                    continue

                sig = self.wallet.sign_transaction(
                    sender=self.wallet.public_key,
                    recipient=transaction_details[0],
                    amount=transaction_details[1],
                )
                print("💸✍🏽 Transaction signature: {}".format(sig))
                if not self.chain.add_transaction(
                    sender = self.wallet.public_key,
                    recipient = transaction_details[0],
                    amount = transaction_details[1],
                    sig = sig
                ):
                    print("💸❌ Adding transaction failed!")
            elif user_choice == "2":
                if not self.chain.mine_block():
                    print("⛏❌ Mining failed!")
            elif user_choice == "3":
                self.print_blockchain_elements()
            elif user_choice == "4":
                participant = self.get_participant()
                print(
                    "Balance of {} is: {:6.3f}".format(
                        participant, self.chain.get_balance(participant)
                    )
                )
            elif user_choice == "5":
                # Create new wallet, create keys
                self.wallet.create_keys()
                self.chain = Blockchain(self.wallet.public_key)
                print(
                    "💰 Wallet with public key {} created!".format(
                        self.wallet.public_key
                    )
                )
            elif user_choice == "6":
                # Load keys from wallet.txt
                self.wallet.load_keys()
                print(
                    "💰 Wallet with public key {} loaded!".format(self.wallet.public_key)
                )
                self.chain = Blockchain(self.wallet.public_key)
            elif user_choice == "7":
                self.wallet.save_keys()
                print(
                    "💰 Wallet with public key {} saved to wallet.txt".format(
                        self.wallet.public_key
                    )
                )
            elif user_choice == "q":
                waiting_for_input = False
            else:
                print("Input was invalid, please pick a value from the list!")

            if not self.chain.verify_chain():
                print("Invalid blockchain!")
                waiting_for_input = False

        print("Done!")

    def get_user_choice(self):
        """
        Utility function to get user input
        """
        user_input = input("Your choice: ")
        return user_input

    def get_participant(self):
        """
        Utility function to get participant's name
        """
        user_input = input("Enter name of participant: ")
        return user_input

    def print_blockchain_elements(self):
        """
        Outputting all blocks in the blockchain
        """
        for block in self.chain.get_blockchain():
            print(block)

    def get_transaction_details(self):
        """
        Gets user input for sender, recipient and amount for a transaction
        """
        recipient = input("Enter recipient address: ")
        amount = float(input("Enter transaction amount: "))
        return (recipient, amount)


if __name__ == "__main__":
    # Initialisation of node upon script execution
    node = Node()
