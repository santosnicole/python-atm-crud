from dao.json_loader import JSONLoader
import random
from datetime import datetime

class CardService:
    def __init__(self, file_path):
        self.file_path = file_path
        self.loader = JSONLoader(file_path)
        self.data = self.loader.load()
        if 'card_holders' not in self.data:
            self.data['card_holders'] = []

    def get_card_details(self, card_number):
        for card_holder in self.data.get('card_holders', []):
            if card_holder['card_number'] == card_number:
                return card_holder
        return {}

    def get_transactions(self, card_number):
        card_details = self.get_card_details(card_number)
        return card_details.get('transactions', [])

    def verify_card_credentials(self, card_number, password):
        card_details = self.get_card_details(card_number)
        return (card_details.get('card_number') == card_number and
                card_details.get('card_password') == password)

    def toggle_card_status(self, card_number):
        card_details = self.get_card_details(card_number)
        if card_details:
            current_status = card_details.get('card_status')
            if current_status == 'active':
                card_details['card_status'] = 'inactive'
            else:
                card_details['card_status'] = 'active'
            self.loader.save(self.data)
            return card_details['card_status']
        return None

    def create_card_holder(self, name, password):
        card_number = self._generate_card_number()
        new_card = {
            "card_number": card_number,
            "name": name,
            "card_password": password,
            "card_status": "inactive",  # Default status
            "card_balance": 0.0,        # Default balance
            "transactions": []
        }
        self.data['card_holders'].append(new_card)
        self.loader.save(self.data)
        return new_card

    def add_credit(self, card_number, amount, description):
        card_details = self.get_card_details(card_number)
        if card_details:
            if card_details.get('card_status') == 'active':
                card_balance = card_details.get('card_balance', 0.0)
                card_balance += amount
                card_details['card_balance'] = card_balance

                transaction = {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "description": description,
                    "transaction_type": "credit",
                    "amount": amount,
                    "balance": card_balance
                }
                card_details['transactions'].append(transaction)
                self.loader.save(self.data)
                return card_details
            else:
                print("Card is inactive.")
        return None

    def use_debit(self, card_number, amount, description):
        card_details = self.get_card_details(card_number)
        if card_details:
            if card_details.get('card_status') == 'active':
                card_balance = card_details.get('card_balance', 0.0)
                if card_balance >= amount:
                    card_balance -= amount
                    card_details['card_balance'] = card_balance

                    transaction = {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "description": description,
                        "transaction_type": "debit",
                        "amount": amount,
                        "balance": card_balance
                    }
                    card_details['transactions'].append(transaction)
                    self.loader.save(self.data)
                    return card_details
                else:
                    print("Insufficient balance.")
            else:
                print("Card is inactive.")
        return None

    def _generate_card_number(self):
        existing_numbers = [ch['card_number'] for ch in self.data.get('card_holders', [])]

        while True:
            new_number = random.randint(1000000000000000, 9999999999999999)
            new_number_str = str(new_number).zfill(16)
            formatted_number = f"{new_number_str[:4]}-{new_number_str[4:8]}-{new_number_str[8:12]}-{new_number_str[12:]}"
            
            if formatted_number not in existing_numbers:
                return formatted_number
