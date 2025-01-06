import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from websocket import create_connection
import json
import time

# Title
st.title("Live Bitcoin Transaction Visualization")

# Use session state for toggle
if "start" not in st.session_state:
    st.session_state.start = False

# Button for start/stop visualization
if st.button("START VISUALIZATION"):
    st.session_state.start = not st.session_state.start  # Toggle start state

if st.session_state.start:
    st.write("Visualization Running... (Press the button again to stop)")
    # Simulate real-time data visualization
    while st.session_state.start:
        # Creating a dummy network graph for visualization
        G = nx.Graph()
        G.add_edge("Bitcoin Wallet A", "Bitcoin Wallet B", weight=5)
        G.add_edge("Bitcoin Wallet B", "Bitcoin Wallet C", weight=10)

        # Draw the network graph
        pos = nx.spring_layout(G)
        weights = nx.get_edge_attributes(G, "weight")
        nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=3000, font_size=10)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=weights)

        # Display the plot
        st.pyplot(plt)
        plt.clf()  # Clear the plot for the next update

        # Wait for 1 second before updating (simulating real-time)
        time.sleep(1)

else:
    st.write("Visualization Paused! Press the button to start.")

