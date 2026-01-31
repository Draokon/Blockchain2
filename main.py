import random
import string
from typing import List

char_map ={'a': '2', 'b': '3', 'c': '5', 'd': 'k', 'e': 'o', 'f': 'd', 'g': 'a', 'h': '9', 'i': '1', 'j': 'H', 'k': '4', 'l': 'O', 'm': 'T', 'n': '7',
          'o': '8', 'p': 'R', 'q': 'S', 'r': '6', 's': 'U', 't': 'V', 'u': 'W', 'v': 'X', 'w': 'Y', 'x': 'Z', 'y': '0', 'z': 'Q', 'A': 'p', 'B': '9', 'C': 'h',
            'D': 'n', 'E': '+', 'F': 'j', 'G': 'A', 'H': 'Y', 'I': 'v', 'J': 'S', 'K': '6', 'L': '11', 'M': 'c', 'N': 'P', 'O': 'aa', 'P': 'Q', 'Q': '97', 'R': '2', 'S': 'jk', 
            'T': 'k', 'U': 'B', 'V': '2c', 'W': '6g', 'X': 'p5', 'Y': '0', 'Z': 'Qq', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
              '!': '-', '@': '=', '#': '+', '$': '[', '%': ']', '^': '{', '&': '}', '*': ';', ':' : '5-', '(': ',', ')': '.', '-': '<', '=': '>', '+': '/', '[': '?', ']': '~', '{': '`', '}': ' '}

salt = 'asr3ophcg5juo6'  

def substitute(text: str) -> str:
    out = []
    for ch in text:
        out.append(char_map.get(ch, ch))
    return ''.join(out)

def insert_salt(text: str) -> str:
    mid = len(text) // 2
    return text[:mid] + salt + text[mid:]

def move_pairs(text: str) -> str:
    text = list(text)
    for i in range(0, len(text)-1, 2):
        text[i], text[i+1] = text[i+1], text[i]
    return ''.join(text)

def add_letters(text: str) -> str:
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    res = []
    for ch in text:
        res.append(ch)
        if ch in alphabet:
            idx = alphabet.index(ch)
            res.append(alphabet[(idx + 5) % len(alphabet)])
    return ''.join(res)
#keicia kas 3 simbolius vietomis
def swap(text: str) -> str:
    if len(text) % 3 != 0:
        text += 'x'
    out = []
    for i in range(0, len(text), 3):
        seg = text[i:i+3]
        out.append(seg[::-1])
    return ''.join(out)

def hash(text: str) -> str:
    s = substitute(text)
    s = insert_salt(s)
    s = add_letters(s)
    s = move_pairs(s)
    s = swap(s)

    total = 0
    for i, ch in enumerate(s):
        total += ord(ch) * (i + 1)

    # sujungiam dar su keliais baitais iš s, kad būtų mažiau kolizijų
    tail = sum(ord(c) for c in s[-8:]) if len(s) >= 8 else sum(ord(c) for c in s)
    total = (total ^ tail) & ((1 << 64) - 1)  # riboja i 64 bit

    # grąžinam hex string
    hexstr = hex(total)[2:].rjust(16, '0')  # 16 simbolių, užpildyta nuliais
    return hexstr
          
# OOP: user

class User:
    def __init__(self, name: str, balance: int):
        self.name = name
        self.balance = balance
        # public_key paprastas string (pvz.: vardas+atsitiktinis)
        self.public_key = f"{name}_{random.randint(1000,9999)}"

    def __repr__(self):
        return f"User({self.name}, bal={self.balance})"

    @staticmethod    
    def random_name(length: int) -> str:
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length)).capitalize()

def generate_users(count=10) -> list['User']:
    users = []
    for _ in range(count):
        name = User.random_name(6)
        balance = round(random.uniform(0, 1000), 2)
        users.append(User(name, balance))
    return users
#OOP: transaction
class Transaction:
    def __init__(self, sender: User, receiver: User, amount: int):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        #trasaction id = hash of sender+receiver+amount+random
        self.tx_id = hash(f"{sender.public_key}->{receiver.public_key}:{amount}:{random.randint(1000,9999)}")
        #Balanso tikrinimas
        if sender.balance < amount:
            raise ValueError("Insufficient balance for transaction")
    def __repr__(self):
        return f"Transaction({self.sender.name} -> {self.receiver.name}, amount={self.amount}, tx_id={self.tx_id})"
              #transakcijos Id tikrinimas
    def verify(self) -> bool:
        expected = hash(f"{self.sender.public_key}->{self.receiver.public_key}:{self.amount}")
        return self.tx_id == expected
# test
tx = Transaction(user, User("Alice", 50), 25)
print(tx)
print(tx.tx_id)

# OOP: block
class Block:
    def __init__(self, transactions: list[Transaction], previous_hash: str):
        self.transactions = transactions
        self.previous_hash = previous_hash
        # block hash = hash of all tx_ids + previous_hash
        tx_data = ''.join(tx.tx_id for tx in transactions)
        self.block_hash = hash(f"{tx_data}:{previous_hash}")
    def __repr__(self):
        return f"Block(num_tx={len(self.transactions)}, prev_hash={self.previous_hash}, block_hash={self.block_hash})"
# test
block = Block([tx], "0000000000000000")
print(block)
print(block.block_hash)
# Some tests

print("Random users:")
print(generate_users(5))
print(hash("Hello"))
user = User("John", 100)
print(user)
print("Public key:", user.public_key)
#tests
print(hash("Hello"))
user = User("John", 100)
print(user)
print(user.public_key)
