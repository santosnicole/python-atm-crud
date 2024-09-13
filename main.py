from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
import random
import json

app = FastAPI()

# Sample data structure
data = {
    "card_holders": []
}

# Load and Save data functions (for demonstration, using global data)
def load_data():
    global data
    try:
        with open('data/cards.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"card_holders": []}

def save_data():
    with open('data/cards.json', 'w') as file:
        json.dump(data, file, indent=4)

# Model Definitions with Examples
class CardHolder(BaseModel):
    name: str = Field(..., example="John Doe")
    card_password: str = Field(..., example="securepassword")
    birthday: str = Field(..., example="1990-01-01")  # Format: YYYY-MM-DD

class Transaction(BaseModel):
    description: str = Field(..., example="Bank Transfer")
    amount: float = Field(..., example=100.0)

class CardDetails(CardHolder):
    card_number: str = Field(..., example="1234-5678-9876-5432")
    card_status: str = Field(..., example="inactive")
    card_balance: float = Field(..., example=0.0)
    transactions: List[dict] = Field(..., example=[
        {"date": "2024-09-12", "description": "Grocery Store", "transaction_type": "debit", "amount": 50.75, "balance": 1249.25},
        {"date": "2024-09-10", "description": "Salary Credit", "transaction_type": "credit", "amount": 1500.00, "balance": 1300.00}
    ])

# Helper Functions
def find_card(card_number):
    return next((card for card in data['card_holders'] if card['card_number'] == card_number), None)

def find_card_by_name_and_birthday(name: str, birthday: str):
    return next((card for card in data['card_holders'] if card['name'] == name and card['birthday'] == birthday), None)

def generate_card_number():
    while True:
        new_number = random.randint(1000000000000000, 9999999999999999)
        new_number_str = str(new_number).zfill(16)
        formatted_number = f"{new_number_str[:4]}-{new_number_str[4:8]}-{new_number_str[8:12]}-{new_number_str[12:]}"
        if not find_card(formatted_number):
            return formatted_number

# Routes
@app.post("/signup", response_model=CardDetails)
def signup(card: CardHolder):
    load_data()
    existing_card = find_card_by_name_and_birthday(card.name, card.birthday)
    if existing_card:
        raise HTTPException(
            status_code=400,
            detail="Card with the same name and birthday already exists. If you don't currently have any existing account with Bank of Bangko, please go to the nearest office."
        )
    
    card_number = generate_card_number()
    new_card = {
        "card_number": card_number,
        "name": card.name,
        "card_password": card.card_password,
        "birthday": card.birthday,
        "card_status": "inactive",
        "card_balance": 0.0,
        "transactions": []
    }
    data['card_holders'].append(new_card)
    save_data()
    return new_card

@app.post("/login")
def login(card_number: str, card_password: str):
    load_data()
    card = find_card(card_number)
    if card and card['card_password'] == card_password:
        return {"message": "Login successful!"}
    raise HTTPException(status_code=401, detail="Invalid card number or password")

@app.post("/toggle-status")
def toggle_status(card_number: str):
    load_data()
    card = find_card(card_number)
    if card:
        card['card_status'] = 'active' if card['card_status'] == 'inactive' else 'inactive'
        save_data()
        return {"card_status": card['card_status']}
    raise HTTPException(status_code=404, detail="Card not found")

@app.post("/add-credit")
def add_credit(card_number: str, transaction: Transaction):
    load_data()
    card = find_card(card_number)
    if card:
        if card['card_status'] == 'active':
            card['card_balance'] += transaction.amount
            card['transactions'].append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "description": transaction.description,
                "transaction_type": "credit",
                "amount": transaction.amount,
                "balance": card['card_balance']
            })
            save_data()
            return {"card_balance": card['card_balance']}
        raise HTTPException(status_code=400, detail="Card is inactive")
    raise HTTPException(status_code=404, detail="Card not found")

@app.post("/use-debit")
def use_debit(card_number: str, transaction: Transaction):
    load_data()
    card = find_card(card_number)
    if card:
        if card['card_status'] == 'active':
            if card['card_balance'] >= transaction.amount:
                card['card_balance'] -= transaction.amount
                card['transactions'].append({
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "description": transaction.description,
                    "transaction_type": "debit",
                    "amount": transaction.amount,
                    "balance": card['card_balance']
                })
                save_data()
                return {"card_balance": card['card_balance']}
            raise HTTPException(status_code=400, detail="Insufficient balance")
        raise HTTPException(status_code=400, detail="Card is inactive")
    raise HTTPException(status_code=404, detail="Card not found")

@app.get("/transactions")
def get_transactions(card_number: str):
    load_data()
    card = find_card(card_number)
    if card:
        return {"transactions": card['transactions']}
    raise HTTPException(status_code=404, detail="Card not found")
