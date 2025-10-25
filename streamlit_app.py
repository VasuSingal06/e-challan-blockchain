import streamlit as st
import pandas as pd
import threading, time
from blockchain import Blockchain
from simulate_iot import simulate_fastag_data

st.set_page_config(page_title="E-Challan Blockchain Simulator", layout='wide')

# --- initialize or cache blockchain and challan list ---
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()
if 'challans' not in st.session_state:
    st.session_state.challans = []

blockchain = st.session_state.blockchain
challans = st.session_state.challans

st.title("🚗 FASTag E-Challan — Streamlit Simulation (Permissioned-like Blockchain)")

col1, col2 = st.columns([2,1])

with col1:
    st.subheader("Live Violations (simulated)")
    placeholder = st.empty()

with col2:
    st.subheader("Controls & Chain Info")
    auto_generate = st.checkbox("Auto-generate violations (background)", value=True)
    gen_pause = st.slider("Simulation pause (seconds)", 0.5, 5.0, 2.0, 0.5)
    if st.button("Force create block from pending challans"):
        # mine a new block manually
        last_proof = blockchain.last_block['proof']
        proof = blockchain.proof_of_work(last_proof)
        prev_hash = blockchain.hash(blockchain.last_block)
        block = blockchain.create_block(proof, prev_hash)
        st.success(f"Mined block #{block['index']} with {len(block['challans'])} challans.")

    st.write("Current chain length:", len(blockchain.chain))
    st.write("Pending challans:", len(blockchain.pending_challans))

# background worker
def worker_loop(pause):
    gen = simulate_fastag_data(pause)
    for event in gen:
        # if no violation, keep going
        if event['violation_type'] == 'No Violation':
            continue
        # add to blockchain pending challans
        blockchain.add_challan(event)
        # append to session visible list
        challans.append(event)
        # automatically mine small blocks when pending >= N or periodically
        if len(blockchain.pending_challans) >= 2:
            last_proof = blockchain.last_block['proof']
            proof = blockchain.proof_of_work(last_proof)
            prev_hash = blockchain.hash(blockchain.last_block)
            blockchain.create_block(proof, prev_hash)
        # small sleep to allow Streamlit to update view
        time.sleep(0.1)
        if not st.session_state.get('run_worker', True):
            break

if 'worker_thread' not in st.session_state:
    st.session_state.run_worker = auto_generate
    if auto_generate:
        t = threading.Thread(target=worker_loop, args=(gen_pause,), daemon=True)
        st.session_state.worker_thread = t
        t.start()

# react to control changes
st.session_state.run_worker = auto_generate

# Display challans table
if len(challans) == 0:
    placeholder.info('No challans yet — waiting for simulated violations. Enable Auto-generate to start.')
else:
    df = pd.DataFrame(challans)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df_display = df[['timestamp','fastag_id','vehicle_number','violation_type','fine_amount']].sort_values('timestamp', ascending=False)
    placeholder.dataframe(df_display.reset_index(drop=True))

st.markdown("---")
st.subheader("Blockchain (recent blocks)")
# show last 5 blocks
recent = blockchain.chain[-5:]
for b in recent[::-1]:
    st.write(f"Block #{b['index']} — challans: {len(b['challans'])} — prev_hash: {b['previous_hash']}")
    st.json(b)
