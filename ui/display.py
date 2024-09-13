class UI:
    @staticmethod
    def display_main_menu():
        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")

    @staticmethod
    def display_invalid_credentials():
        print("Invalid card number or password. Please try again.")

    @staticmethod
    def prompt_for_card_number():
        return input("Enter card number: ")

    @staticmethod
    def prompt_for_password():
        return input("Enter password: ")

    @staticmethod
    def prompt_for_name():
        return input("Enter name: ")

    @staticmethod
    def display_new_card_holder_success(card):
        print(f"New card created successfully: {card}")

    @staticmethod
    def display_card_menu(card_status, card_balance):
        print(f"Card Status: {'Active' if card_status else 'Inactive'}")
        print(f"Card Balance: ${card_balance:.2f}")
        print("1. Toggle Card Status")
        print("2. Show Transaction History")
        print("3. Add Credits")
        print("4. Use Debit")
        print("5. Logout")

    @staticmethod
    def display_card_status_change(new_status):
        print(f"Card status changed to: {new_status}")

    @staticmethod
    def display_transactions(transactions):
        if not transactions:
            print("No transactions found.")
        else:
            # Reverse the transactions to display from bottom to top
            for txn in reversed(transactions):
                print(f"Date: {txn['date']}, Description: {txn['description']}, Type: {txn['transaction_type']}, Amount: ${txn['amount']:.2f}, Balance: ${txn['balance']:.2f}")

    @staticmethod
    def display_transaction_menu():
        print("1. Go Back")

    @staticmethod
    def display_credit_success(card):
        print(f"Credit added successfully. New balance: ${card['card_balance']:.2f}")

    @staticmethod
    def display_debit_success(card):
        print(f"Debit processed successfully. New balance: ${card['card_balance']:.2f}")
