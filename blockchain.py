import datetime
import hashlib
import json
from flask import Flask, jsonify
import requests
from uuid import uuid4
from urllib.parse import urlparse

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(1, "-")
    
    def create_block(self, proof, previous_hash):
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
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys= True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_valid(self, chain):
        for block_index in range(len(chain)):
            if block_index != 0:
                # check if it still in the chain
                block = chain[block_index]
                previous_block = chain[block_index-1]
                if block["previous_hash"] != self.hash(previous_block):
                    return False
                
                # check whether proof is valid:
                current_proof = block["proof"]
                previous_proof = previous_block["proof"]
                hash_operation = hashlib.sha256(str(current_proof**2-previous_proof**2).encode()).hexdigest()
                if hash_operation[:4] != "0000":
                    return False
        return True

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
                

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
bc = Blockchain()

@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = bc.get_prev_block()
    previous_proof = previous_block["proof"]
    proof = bc.proof_of_work(previous_proof)
    previous_hash = bc.hash(previous_block)
    block = bc.create_block(proof, previous_hash)
    response = {
        "message": "you have succesfully mined a block",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "proof": proof,
        "previous_hash": previous_hash
    }
    return jsonify(response), 200

@app.route('/get_chain', methods = ["GET"])
def get_chain():
    response = {
        "chain": bc.chain,
        "length": len(bc.chain)
    }
    return jsonify(response), 200

@app.route('/is_valid', methods = ['GET'])
def is_valid():
    validation = bc.is_valid(bc.chain)
    if validation:
        response = {
            "message": "the blockchain is valid"
        }
    else:
        response = {
            "message": "the blockchain is invalid"
        }

    return jsonify(response), 200

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    response = request.urlparse
    
app.run(host="0.0.0.0", port=5001)

