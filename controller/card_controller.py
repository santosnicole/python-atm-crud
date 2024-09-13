from service.card_service import CardService

class CardController:
    def __init__(self, file_path):
        self._card_service = CardService(file_path)
    
    def _get_card_details(self, card_number):
        card_details = self._card_service.get_card_details(card_number)
        if not card_details:
            raise ValueError("Card not found.")
        return card_details

    def get_card_details(self, card_number):
        return self._get_card_details(card_number)

    def get_transactions(self, card_number):
        card_details = self._get_card_details(card_number)
        return card_details.get('transactions', [])

    def verify_card_credentials(self, card_number, password):
        card_details = self._get_card_details(card_number)
        return (card_details.get('card_password') == password)

    def toggle_card_status(self, card_number):
        card_details = self._get_card_details(card_number)
        current_status = card_details.get('card_status')
        new_status = 'inactive' if current_status == 'active' else 'active'
        card_details['card_status'] = new_status
        self._card_service.save_data()
        return new_status

    def create_card_holder(self, name, password):
        new_card = self._card_service.create_card_holder(name, password)
        return new_card

    def add_credit(self, card_number, amount, description):
        card_details = self._get_card_details(card_number)
        if card_details.get('card_status') != 'active':
            raise PermissionError("Card is inactive. Cannot add credit.")
        updated_card = self._card_service.add_credit(card_number, amount, description)
        return updated_card

    def use_debit(self, card_number, amount, description):
        card_details = self._get_card_details(card_number)
        if card_details.get('card_status') != 'active':
            raise PermissionError("Card is inactive. Cannot use debit.")
        updated_card = self._card_service.use_debit(card_number, amount, description)
        return updated_card
