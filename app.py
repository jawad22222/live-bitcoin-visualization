import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import time

# Title of the app
st.title("Live Bitcoin Transaction Visualization")

# Initialize session state variables
if "visualization_running" not in st.session_state:
    st.session_state.visualization_running = False

# Function to toggle visualization on/off
def start_stop_visualization():
    st.session_state.visualization_running = not st.session_state.visualization_running

# Button to start/stop visualization
st.button("START VISUALIZATION", on_click=start_stop_visualization)

# Run visualization if the session state is active
if st.session_state.visualization_running:
    st.write("Visualization Running... (Press the button again to stop)")

    # Placeholder for dynamic graph updates
    placeholder = st.empty()

    while st.session_state.visualization_running:
        # Create a graph (example data)
        G = nx.Graph()
        G.add_edge("Wallet A", "Wallet B", weight=5)
        G.add_edge("Wallet B", "Wallet C", weight=10)
        G.add_edge("Wallet C", "Wallet D", weight=15)

        # Draw the graph
        pos = nx.spring_layout(G)
        weights = nx.get_edge_attributes(G, "weight")
        fig, ax = plt.subplots()
        nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=3000, font_size=10, ax=ax)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=weights, ax=ax)

        # Show the graph in placeholder
        with placeholder.container():
            st.pyplot(fig)

        # Clear matplotlib plot to avoid overlapping
        plt.clf()

        # Simulate real-time updates
        time.sleep(1)
else:
    st.write("Visualization Stopped! Press the button to start.")
