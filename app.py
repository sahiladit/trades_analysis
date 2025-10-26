from flask import Flask, render_template, request, jsonify
import sqlite3
import threading
import time
import numpy as np
import pandas as pd
import statsmodels.api as sm 

app = Flask(__name__)

DB_FILE = 'database.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ticks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            symbol TEXT,
            price REAL,
            size REAL
        )
    """)
    conn.commit()
    conn.close()

# Background: Ingest demo data if no stream is connected (simulate tick source for testing)
def ingest_demo_data():
    import random, datetime
    symbols = ['btcusdt', 'ethusdt']
    while True:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        now = datetime.datetime.utcnow().isoformat()
        for sym in symbols:
            price = random.random()*60000
            size = random.random()*10
            cursor.execute("INSERT INTO ticks (timestamp, symbol, price, size) VALUES (?, ?, ?, ?)",
                (now, sym, price, size)
            )
            print(f"Inserted tick: {now}, {sym}, {price}, {size}")
        conn.commit()
        conn.close()
        time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

from flask import request

alerts_config = {
    "zscore_threshold": 2.0
}

@app.route('/api/alerts', methods=['POST'])
def update_alerts():
    global alerts_config
    data = request.json
    # Example payload: {"zscore_threshold": 2.5}
    alerts_config.update(data)
    return jsonify({"status": "success", "alerts_config": alerts_config})

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    return jsonify(alerts_config)


@app.route('/api/analytics')
def analytics():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM ticks ORDER BY timestamp DESC LIMIT 3000", conn)
    conn.close()
    
    symbols = df['symbol'].unique()
    if len(symbols) < 2:
        return jsonify({})  # Need at least two symbols for analytics

    sym1, sym2 = symbols[:2]  # Pick first two symbols for pair analytics
    df1 = df[df['symbol'] == sym1].sort_values('timestamp')
    df2 = df[df['symbol'] == sym2].sort_values('timestamp')

    prices1 = df1['price'].values
    prices2 = df2['price'].values

    # Ensure same length, align by latest
    min_len = min(len(prices1), len(prices2))
    prices1 = prices1[-min_len:]
    prices2 = prices2[-min_len:]

    if min_len < 30:
        return jsonify({})  # Not enough data for regression

    X = sm.add_constant(prices2)
    model = sm.OLS(prices1, X).fit()
    hedge_beta = model.params[1]
    spread = prices1 - hedge_beta * prices2
    z_score = (spread[-1] - spread.mean()) / spread.std() if spread.std() != 0 else 0
    rolling_corr = np.corrcoef(prices1[-100:], prices2[-100:])[0,1] if min_len >= 100 else 0

    result = {
        'sym1': sym1,
        'sym2': sym2,
        'hedge_beta': hedge_beta,
        'last_spread': spread[-1],
        'z_score': z_score,
        'rolling_corr': rolling_corr,
        'prices1': prices1.tolist(),
        'prices2': prices2.tolist(),
        'spread_list': spread.tolist(),
    }

    return jsonify(result)

@app.route('/api/tick', methods=['POST'])
def tick():
    data = request.json
    # Expects: { "timestamp": str, "symbol": str, "price": float, "size": float }
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ticks (timestamp, symbol, price, size) VALUES (?, ?, ?, ?)",
                   (data['timestamp'], data['symbol'], data['price'], data['size']))
    conn.commit()
    conn.close()
    return '', 204


if __name__ == '__main__':
    init_db()
    thread = threading.Thread(target=ingest_demo_data, daemon=True)
    thread.start()
    app.run(debug=True)



