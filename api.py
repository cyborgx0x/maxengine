import json

import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template_string

from core import get_signal

symbols_list = [
    "GBPUSD=X",
    "EURUSD=X",
    "GC=F",
    "JPY=X",
    "AUDUSD=X",
    "NZDUSD=X",
    "EURJPY=X",
    "GBPJPY=X",
    "EURGBP=X",
    "EURCAD=X",
]

app = Flask(__name__)


def distribute_signals(df):
    # Convert DataFrame to an appropriate format for distribution
    # Here, df is the filtered DataFrame with only 'buy' or 'sell' signals

    # Placeholder for distribution code
    # Example: send_email(df), send_telegram(df), send_notification(df)

    pass


def fetch_and_save_signals():
    df = pd.DataFrame()

    for s in symbols_list:
        signal = get_signal(
            s
        )  # Assuming this returns a dict or similar structure with 'signal' key
        df[s] = signal

    df = df.transpose()

    # Filter to include only 'buy' or 'sell' signals
    filtered_df = df[df["signal"].isin(["buy", "sell"])]

    # Save the filtered DataFrame to JSON using the corrected file name
    filtered_df.to_json("filtered_signals.json")

    # After saving, distribute the signals
    distribute_signals(filtered_df)


# Scheduler to run the fetch_and_save_signals function every minute
scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_and_save_signals, trigger="interval", minutes=10)
scheduler.start()


@app.route("/")
def show_dataframe():
    # Read the filtered JSON file into a DataFrame
    try:
        df = pd.read_json("filtered_signals.json")
    except Exception as e:
        return f"Error reading signals: {str(e)}"

    # Convert DataFrame to HTML table with added classes for styling
    html_data = df.to_html(classes="styled-table")

    # HTML with style tag
    return render_template_string(
        """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            .styled-table {
                border-collapse: collapse;
                margin: 25px 0;
                font-size: 0.9em;
                font-family: sans-serif;
                min-width: 400px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
            }
            .styled-table thead tr {
                background-color: #009879;
                color: #ffffff;
                text-align: left;
            }
            .styled-table th,
            .styled-table td {
                padding: 12px 15px;
            }
            .styled-table tbody tr {
                border-bottom: 1px solid #dddddd;
            }
            .styled-table tbody tr:nth-of-type(even) {
                background-color: #f3f3f3;
            }
            .styled-table tbody tr:last-of-type {
                border-bottom: 2px solid #009879;
            }
            .styled-table tbody tr.active-row {
                font-weight: bold;
                color: #009879;
            }
        </style>
    </head>
    <body>
        {{ table|safe }}
    </body>
    </html>
    """,
        table=html_data,
    )


fetch_and_save_signals()

if __name__ == "__main__":
    # Initial fetch before starting the server
    app.run(debug=True)
