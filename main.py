import random
import string
from typing import List
import time

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
    def __init__(self, name: str, balance: float):
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
    def __init__(self, sender: User, receiver: User, amount: float):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        #trasaction id = hash of sender+receiver+amount+random
        self.tx_id = hash(f"{sender.public_key}->{receiver.public_key}:{amount}")
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
              
        self.version = "2.0" # bloko formato versija
        self.timestamp = time.time() 
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.merkle_root = merkle_root([tx.tx_id for tx in transactions])
        self.nonce = 0 
        self.difficulty = difficulty # su kiek nuliu turi prasideti hash
        self.block_hash = None             
    def __repr__(self):
        return f"Block(num_tx={len(self.transactions)}, prev_hash={self.previous_hash}, block_hash={self.block_hash})"
              
# Bloku kasimo bandymas
    def mine(self, max_attempts=100_000, time_limit=5) -> bool:

        target = "0" * self.difficulty
        start_time = time.time()
        attempts = 0

        while attempts < max_attempts and (time.time() - start_time) < time_limit:
            header_string = f"{self.previous_hash}{self.merkle_root}{self.timestamp}{self.version}{self.nonce}{self.difficulty}"
            hash_value = hash(header_string)
            attempts += 1

            if hash_value.startswith(target):
                self.block_hash = hash_value
                print(f"I6kastas blokas. Hash: {self.block_hash}")
                print(f"Bandymu sk: {attempts}")
                return True

            self.nonce += 1

        print(f"Nepavyko iškasti bloko per {attempts} bandymų / {time_limit} s.")
        return False
    
    def __repr__(self):
        return f"Block(num_tx={len(self.transactions)}, prev_hash={self.previous_hash}, block_hash={self.block_hash})"

#blockchain
class Blockchain:
    def __init__(self, difficulty=3):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block([], "0" * 16, self.difficulty)
        genesis.mine()
        self.chain.append(genesis)

    def get_last_hash(self):
        return self.chain[-1].block_hash

    def add_block(self, block: Block):
        self.chain.append(block)


#merkle root 

def merkle_root(tx_ids: List[str]) -> str:
    if not tx_ids:
        return hash('')

    layer = tx_ids[:]
    while len(layer) > 1:
        next_layer = []
        for i in range(0, len(layer), 2):
            left = layer[i]
            right = layer[i + 1] if i + 1 < len(layer) else layer[i]
            combined = left + right
            next_layer.append(hash(combined))
        layer = next_layer
    return layer[0]
          
# test
print("Merkle Root Test:")
tx_ids = [tx.tx_id for tx in [tx]]  
print("Transaction IDs:", tx_ids)
root = merkle_root(tx_ids)
print("Merkle Root:", root)

# dencentralizuotas kasimas

def mine_block_decentralized(transactions: list[Transaction], previous_hash: str, difficulty: int):

    max_attempts = 50000
    time_limit = 5

    while True:
        print("\n Generuojami 5 kandidatų blokai:")

        candidates = []
        for i in range(5):
            block_txs = random.sample(transactions, min(100, len(transactions)))
            block = Block(block_txs, previous_hash, difficulty)
            candidates.append(block)
            print(f" Kandidatas #{i+1} sukurtas su {len(block_txs)} transakcijų")

        for i, block in enumerate(candidates, 1):
            print(f"\n Bandome kasti kandidatą #{i}")
            success = block.mine(max_attempts=max_attempts, time_limit=time_limit)
            if success:
                print(f"Kandidatas #{i} laimėjo kasimą!")
                return block

        print("\n Nė vienas blokas neiškastas. Didiname ribas ir kartojame...")
        max_attempts *= 2
        time_limit += 5


# pagrindine prog
if __name__ == "__main__":
    print(" Generuojami vartotojai...")
    users = generate_users(1000)

    print(" Generuojamos transakcijos...")
    transactions = []
    while len(transactions) < 10000:
        sender, receiver = random.sample(users, 2)
        amount = round(random.uniform(1, min(sender.balance, 10000)), 2)
        try:
            tx = Transaction(sender, receiver, amount)
            transactions.append(tx)
        except ValueError:
            continue

    print(" Inicijuojama Blockchain...")
    blockchain = Blockchain(difficulty=3)

    block_number = 1
    while transactions:
        print(f"\n Formuojamas blokas #{block_number}")

        # Pasirenkama apie 100 treansakciju blokui
        selected_txs = random.sample(transactions, min(100, len(transactions)))

        # Tikriname transakcijas
        valid_txs = []
        for tx in selected_txs:
            if tx.verify() and tx.sender.balance >= tx.amount:
                valid_txs.append(tx)

        # Kasimas decentralizuotu budu
        block = mine_block_decentralized(valid_txs, blockchain.get_last_hash(), difficulty=3)

        # Atnaujiname balansus ir pasaliname transakcijas is saraso
        for tx in valid_txs:
            tx.sender.balance -= tx.amount
            tx.receiver.balance += tx.amount
            transactions.remove(tx)

        blockchain.add_block(block)
        print(f" Blokas #{block_number} pridėtas į grandinę")
        block_number += 1

    print("\n Visos transakcijos apdorotos")
    print(f" Iš viso blokų: {len(blockchain.chain)}")


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
