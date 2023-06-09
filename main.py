import datetime
import hashlib
import json
from flask import Flask, jsonify

class Blockchain:
    def __init__(self):
        self.chain = []
    
    def create_block(self, proof=1, previous_hash=0):
        block = {
            'index': len(self.chain)+1,
            'timestamp': str(datetime.datetime.now()),
            'proof' : proof,
            'previous_hash': previous_hash,
        }
        self.chain.append(block)
        return block
    
    def get_prev_block(self):
        return self.chain[-1]


app = Flask(__name__)
bc = Blockchain()
block = bc.create_block(1, 0)
print(block)
