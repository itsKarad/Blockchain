from blockchain import Blockchain
from uuid import uuid4


class Node:
    def __init__(self):
        self.node_id = str(uuid4())
        self.chain = Blockchain(self.node_id)
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
        print("5: Get all participants")
        print("6: Check validity of transactions")
        print("h: Manipulate the chain")
        print("q: Quit")
        while waiting_for_input:
            print("*" * 40)
            user_choice = self.get_user_choice()
            if user_choice == "1":
                transaction_details = self.get_transaction_details()
                self.chain.add_transaction(
                    transaction_details[0],
                    transaction_details[1],
                    transaction_details[2],
                )
            elif user_choice == "2":
                self.chain.mine_block()
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
                print(self.chain.participants)
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
        sender = input("Enter sender address: ")
        recipient = input("Enter recipient address: ")
        amount = float(input("Enter transaction amount: "))
        return (sender, recipient, amount)


# Initialisation of node upon script execution
node = Node()
