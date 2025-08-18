"""
Analyzes and plots the simulation log data.
"""

import pandas as pd
import matplotlib.pyplot as plt
import config

def analyze_log():
    """Reads the simulation log and plots the data."""
    try:
        df = pd.read_csv(config.LOG_FILE)
    except FileNotFoundError:
        print(f"Log file not found: {config.LOG_FILE}")
        return

    if df.empty:
        print("Log file is empty.")
        return

    plt.figure(figsize=(12, 8))
    plt.plot(df['Second'] / (24 * 3600), df['Healthy'], label='Healthy')
    plt.plot(df['Second'] / (24 * 3600), df['Exposed'], label='Exposed')
    plt.plot(df['Second'] / (24 * 3600), df['Infected'], label='Infected')
    plt.plot(df['Second'] / (24 * 3600), df['Recovered'], label='Recovered')
    plt.plot(df['Second'] / (24 * 3600), df['Dead'], label='Dead')

    plt.xlabel("Days")
    plt.ylabel("Population")
    plt.title("Disease Spread Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    analyze_log()
