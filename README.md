# FASTag E-Challan Blockchain Simulator (Streamlit)

This project is a lightweight, virtual simulation of a FASTag-integrated e-challan system with
a simple permissioned-like blockchain implemented in Python. It runs entirely in the cloud (no hardware).
The UI uses Streamlit for a quick demo dashboard that updates with simulated violations and stores
them immutably in a Python blockchain structure.

## Files
- `blockchain.py` — Simple SHA-256 blockchain implementation (proof-of-work with low difficulty).
- `simulate_iot.py` — Generator that simulates FASTag detections and violation events.
- `streamlit_app.py` — Main Streamlit app (run this to start the demo).
- `requirements.txt` — Python requirements.

## How to run (Replit / Codespaces / Local)
1. Install requirements: `pip install -r requirements.txt`
2. Run the Streamlit app: `streamlit run streamlit_app.py --server.port 8501 --server.enableCORS false`
3. Open the forwarded port (8501). In Codespaces, use the Ports view and open in browser.

## Notes
- This is a simulation and keeps all data in memory. For persistence, connect to SQLite or a DB.
- For a permissioned blockchain demo (Hyperledger Fabric), replace the blockchain layer accordingly.
- The proof-of-work is intentionally low-cost for demo speed.
