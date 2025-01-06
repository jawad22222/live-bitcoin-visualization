import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import networkx as nx
import matplotlib.pyplot as plt
import time

# Selenium WebDriver Setup
def get_driver():
    service = Service("/path/to/chromedriver")  # Update path to ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run browser in headless mode
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Scrape data from DailyBlockchain
def fetch_live_data(driver):
    url = "https://dailyblockchain.github.io/"
    driver.get(url)
    time.sleep(2)  # Allow time for the page to load

    # Scrape input, output, and transactions
    inputs = driver.find_element(By.XPATH, "(//div[@class='stat-number'])[1]").text
    outputs = driver.find_element(By.XPATH, "(//div[@class='stat-number'])[2]").text
    transactions = driver.find_element(By.XPATH, "(//div[@class='stat-number'])[3]").text

    # Scrape graph data (nodes and edges)
    nodes = driver.find_elements(By.TAG_NAME, "circle")
    edges = driver.find_elements(By.TAG_NAME, "line")

    graph_data = {
        "inputs": int(inputs.replace(",", "")),
        "outputs": int(outputs.replace(",", "")),
        "transactions": int(transactions.replace(",", "")),
        "nodes": len(nodes),
        "edges": len(edges),
    }
    return graph_data

# Visualize the graph
def draw_graph(graph_data):
    G = nx.DiGraph()
    # Create random edges for now (adjust if scraping actual data)
    for i in range(graph_data["nodes"]):
        G.add_node(i)
    for i in range(graph_data["edges"]):
        G.add_edge(i % graph_data["nodes"], (i + 1) % graph_data["nodes"])

    # Plot graph
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, arrowsize=15)
    st.pyplot(plt)

# Streamlit App
st.title("DailyBlockchain Live Bitcoin Visualization")

# WebDriver Initialization
driver = get_driver()

# Live Update Loop
while True:
    try:
        # Fetch live data
        live_data = fetch_live_data(driver)

        # Display live metrics
        st.subheader("Live Bitcoin Metrics")
        st.metric("Input Transactions", live_data["inputs"])
        st.metric("Output Transactions", live_data["outputs"])
        st.metric("Total Transactions", live_data["transactions"])

        # Display graph visualization
        st.subheader("Live Bitcoin Transaction Graph")
        draw_graph(live_data)

        # Wait before refreshing
        time.sleep(2)
    except Exception as e:
        st.error(f"Error: {e}")
        break



