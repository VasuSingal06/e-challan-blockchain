import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_challans = []
        # create genesis block
        self.create_block(proof=100, previous_hash='1')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'challans': self.pending_challans.copy(),
            'proof': proof,
            'previous_hash': previous_hash
        }
        # reset pending challans and append block
        self.pending_challans = []
        self.chain.append(block)
        return block

    def add_challan(self, challan):
        self.pending_challans.append(challan)
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    def hash(self, block):
        # We must ensure consistency: sort keys
        block_str = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_str).hexdigest()

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    def valid_proof(self, last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        # simple difficulty - leading zeros
        return guess_hash[:4] == '0000'
