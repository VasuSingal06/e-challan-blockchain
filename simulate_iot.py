import random
import time

def simulate_fastag_data(pause=2.0):
    """Generator that yields simulated FASTag violation events."""
    fastags = ["FTG123", "FTG456", "FTG789", "FTG999", "FTG321", "FTG654"]
    violations = ["Overspeeding", "Red Light Jump", "Wrong Lane", "No FASTag", "No Violation"]

    while True:
        vehicle = random.choice(fastags)
        violation = random.choices(violations, weights=[0.3,0.2,0.15,0.05,0.3])[0]
        event = {
            "fastag_id": vehicle,
            "vehicle_number": f"DL{random.randint(1,9)}AB{random.randint(1000,9999)}",
            "violation_type": violation,
            "fine_amount": 0 if violation=="No Violation" else random.choice([500,1000,1500,2000]),
            "timestamp": time.time()
        }
        # only yield actual violations (optionally include No Violation)
        yield event
        time.sleep(pause)
