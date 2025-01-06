import streamlit as st
import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
import time

# Streamlit app title
st.title("Live Bitcoin Transaction Visualization")

# Function to scrape live data from DailyBlockchain
def fetch_bitcoin_data():
    url = "https://dailyblockchain.github.io/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extracting the live numbers (inputs, outputs, and transactions)
    live_data = soup.find_all("div", class_="stat-number")
    input_transactions = int(live_data[0].text.strip())
    output_transactions = int(live_data[1].text.strip())
    total_transactions = int(live_data[2].text.strip())

    # Extracting graph data (for visualization)
    graph_data = []
    nodes = soup.find_all("circle")
    links = soup.find_all("line")

    for node in nodes:
        graph_data.append(node["id"])  # Replace with actual attributes if available

    edges = [(link["source"], link["target"]) for link in links]  # Adjust attributes if needed

    return {
        "input_transactions": input_transactions,
        "output_transactions": output_transactions,
        "total_transactions": total_transactions,
        "graph_data": edges,
    }

# Function to draw the graph
def draw_graph(graph_data):
    G = nx.DiGraph()
    G.add_edges_from(graph_data)

    # Draw the graph with custom styling
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, arrowsize=15)
    st.pyplot(plt)

# Real-time display of metrics and graph
st.write("Visualization Running...")

while True:
    try:
        # Fetch live data
        data = fetch_bitcoin_data()

        # Display live metrics
        st.subheader("Live Bitcoin Transactions")
        st.metric("Input Transactions", data["input_transactions"])
        st.metric("Output Transactions", data["output_transactions"])
        st.metric("Total Transactions", data["total_transactions"])

        # Display graph visualization
        st.subheader("Live Bitcoin Transaction Graph")
        draw_graph(data["graph_data"])

        # Real-time update interval
        time.sleep(2)

    except Exception as e:
        st.error(f"Error fetching data: {e}")


