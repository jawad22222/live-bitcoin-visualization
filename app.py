import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from websocket import create_connection
import json

st.title("Live Bitcoin Transaction Visualization")
st.markdown("### Inputs, Outputs, and Transactions")

# Live stats placeholders
input_count = st.empty()
output_count = st.empty()
transaction_count = st.empty()

# Graph creation
G = nx.DiGraph()
pos = {}

# Initialize counts
input_cnt = 0
output_cnt = 0
transaction_cnt = 0

# WebSocket connection
def fetch_data():
    global input_cnt, output_cnt, transaction_cnt
    ws = create_connection("wss://ws.blockchain.info/inv")
    ws.send(json.dumps({"op": "unconfirmed_sub"}))

    while True:
        try:
            data = ws.recv()
            message = json.loads(data)
            if message.get("op") == "utx":
                tx_hash = message["x"]["hash"]
                inputs = message["x"]["inputs"]
                outputs = message["x"]["out"]

                # Add transaction node
                G.add_node(tx_hash, type="transaction")
                pos[tx_hash] = (0, 0)  # Dummy position

                for input_item in inputs:
                    addr = input_item["prev_out"].get("addr", "unknown")
                    value = input_item["prev_out"].get("value", 0)
                    G.add_node(addr, type="input", value=value)
                    G.add_edge(addr, tx_hash)
                    input_cnt += 1

                for output_item in outputs:
                    addr = output_item.get("addr", "unknown")
                    value = output_item.get("value", 0)
                    G.add_node(addr, type="output", value=value)
                    G.add_edge(tx_hash, addr)
                    output_cnt += 1

                transaction_cnt += 1
                update_live_stats()

                # Visualize after every transaction
                if transaction_cnt % 5 == 0:
                    visualize_graph()
        except Exception as e:
            print("Error:", e)
            break

    ws.close()

# Update stats
def update_live_stats():
    input_count.text(f"Inputs: {input_cnt}")
    output_count.text(f"Outputs: {output_cnt}")
    transaction_count.text(f"Transactions: {transaction_cnt}")

# Visualize graph
def visualize_graph():
    plt.figure(figsize=(10, 7))
    nx.draw_networkx(G, pos, with_labels=False, node_size=50, alpha=0.7, edge_color="gray")
    plt.title("Live Bitcoin Transaction Network")
    plt.axis("off")
    st.pyplot(plt.gcf())
    plt.close()

# Run fetch_data in the background
st.button("Start Visualization", on_click=fetch_data)
