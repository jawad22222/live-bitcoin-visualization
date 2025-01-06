import streamlit as st
import requests
import json
import networkx as nx
import matplotlib.pyplot as plt
import time

# Streamlit app title
st.title("Live Bitcoin Transaction Visualization")

# Session state variables for toggle and data
if "visualization_running" not in st.session_state:
    st.session_state.visualization_running = False

# Function to start/stop visualization
def start_stop_visualization():
    st.session_state.visualization_running = not st.session_state.visualization_running

# Button for starting/stopping visualization
st.button("START VISUALIZATION", on_click=start_stop_visualization)

# Placeholder for metrics and graph
placeholder_metrics = st.empty()
placeholder_graph = st.empty()

# Function to fetch live data from the website's API
def fetch_bitcoin_data():
    # Example of scraping (replace URL with actual API or endpoint if available)
    url = "https://dailyblockchain.github.io/"
    response = requests.get(url)

    # If there is a backend API, modify this part
    # Assuming the response contains JSON-like data
    # Replace below simulation with actual data extraction logic
    data = {
        "input_transactions": 200,  # Replace this with actual data
        "output_transactions": 180,  # Replace this with actual data
        "total_transactions": 380,  # Replace this with actual data
        "graph_data": [
            ("Wallet1", "Wallet2"),
            ("Wallet2", "Wallet3"),
            ("Wallet3", "Wallet4"),
        ]  # Simulated graph data
    }

    return data

# Function to draw the graph
def draw_graph(graph_data):
    G = nx.DiGraph()  # Directed graph
    G.add_edges_from(graph_data)

    # Drawing the graph
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="lightblue", font_size=10, font_weight="bold", arrowsize=20)
    st.pyplot(plt)

# Run visualization if the toggle is active
if st.session_state.visualization_running:
    st.write("Visualization Running... (Press the button again to stop)")
    while st.session_state.visualization_running:
        # Fetch live data
        data = fetch_bitcoin_data()

        # Display metrics
        with placeholder_metrics.container():
            st.subheader("Real-Time Bitcoin Transactions")
            st.metric("Input Transactions", data["input_transactions"])
            st.metric("Output Transactions", data["output_transactions"])
            st.metric("Total Transactions", data["total_transactions"])

        # Display live graph
        with placeholder_graph.container():
            st.subheader("Live Bitcoin Transaction Graph")
            draw_graph(data["graph_data"])

        # Real-time update interval
        time.sleep(2)
else:
    st.write("Visualization Stopped! Press the button to start.")

