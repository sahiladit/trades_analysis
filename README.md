# Binance Futures Collector & Analytics Dashboard

A local, real-time analytics dashboard for quantitative research, trading, and strategy monitoring. Ingests, stores, and visualizes Binance futures tick data, with advanced statistical analytics, custom alerts, and data export — 100% locally run in your browser.

---

## 🚀 Features

- **Live Data Ingestion:** Stream tick data from Binance perpetual futures via browser WebSocket.
- **Persistent Storage:** Every tick recorded in SQLite for analytics/backtesting.
- **Statistical Analytics:**
  - Hedge ratio & spread
  - Z-score, rolling correlation
  - **Max drawdown, win/loss streak calculations**
  - Liquidity summaries and cross-correlation heatmap
- **Alerting:** User-defined threshold alert (popup) for z-score or other analytics.
- **Export/Download:**  
  - Analytics and tick dataset as CSV or NDJSON at any time
- **Offline by Design:**  
  No external cloud or accounts required; privacy and speed guaranteed.

---

## Languages / Libraries
- Python
- Javascript
- HTML and CSS
- sqlite
- Flask
- numpy and Pandas
- statsmodel

## 🛠️ Setup


```bash
git clone <your_repo_url>
cd <your_repo>
pip install -r requirements.txt
python3 app.py or python app.py
```

## 💡 ChatGPT/AI Usage Transparency

Parts of this code, helper scripts, and statistical design were created with the support of ChatGPT. Prompts included:
- "Add a graph to show the statistics of the data"
- "Write a code to add the data in the CSV file."
- "Suggest tools to show analytics in easy manner."

Basic prompt engineering was used which included using """ for input , giving contexts to ChatGPT , using basic English , providing clear goals etc.

---

