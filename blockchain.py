import hashlib
import json
import smtplib
from email.mime.text import MIMEText
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

        # Send email notification (only for actual violations)
        if challan.get("violation_type") != "No Violation":
            try:
                self.send_email(challan["email"], challan)
            except Exception as e:
                print(f"⚠️ Failed to send email to {challan['email']}: {e}")

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

    def send_email(self, to_email, challan):
        """Send an email notification for a new challan."""
        sender = "esportspubggaming1234@gmail.com"  
        password = "rfsnvbfbakvspazx"

        subject = "🚨 New E-Challan Notification"
        body = (
            f"Dear user,\n\n"
            f"A new challan has been issued against your vehicle.\n\n"
            f"Vehicle Number: {challan['vehicle_number']}\n"
            f"Violation: {challan['violation_type']}\n"
            f"Fine Amount: ₹{challan['fine_amount']}\n"
            f"FASTag ID: {challan['fastag_id']}\n\n"
            f"Timestamp: {time()}\n\n"
            f"Thank you,\nFASTag E-Challan System"
        )

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = to_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)

        print(f"📧 Email sent successfully to {to_email}")
