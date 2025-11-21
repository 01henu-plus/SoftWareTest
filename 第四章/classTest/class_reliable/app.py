from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_FILE = 'orders.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, item TEXT, qty INTEGER, status TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS inventory (item TEXT PRIMARY KEY, stock INTEGER)')
    cursor.execute("DELETE FROM inventory")
    cursor.execute("INSERT OR REPLACE INTO inventory VALUES ('book', 100)")
    cursor.execute("INSERT OR REPLACE INTO inventory VALUES ('pen', 200)")
    conn.commit()
    conn.close()

@app.route('/health', methods=['GET'])
def health():
    try:
        conn = sqlite3.connect(DB_FILE, timeout=2)
        conn.execute("SELECT 1")
        conn.close()
        return jsonify({"status": "healthy"}), 200
    except:
        return jsonify({"status": "unhealthy"}), 503

@app.route('/order', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        item = data.get('item')
        qty = data.get('qty', 0)
        
        if not item or qty <= 0:
            return jsonify({"status": "error", "message": "Invalid input"}), 400
        
        conn = sqlite3.connect(DB_FILE, timeout=5)
        cursor = conn.cursor()
        cursor.execute("SELECT stock FROM inventory WHERE item=?", (item,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return jsonify({"status": "error", "message": "Item not found"}), 400
        
        if result[0] < qty:
            conn.close()
            return jsonify({"status": "error", "message": "Insufficient stock"}), 400
        
        cursor.execute("INSERT INTO orders (item, qty, status) VALUES (?, ?, 'completed')", (item, qty))
        cursor.execute("UPDATE inventory SET stock = stock - ? WHERE item = ?", (qty, item))
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": "Order created"}), 200
    except sqlite3.OperationalError:
        return jsonify({"status": "error", "message": "Database error"}), 503
    except:
        return jsonify({"status": "error", "message": "Server error"}), 500

if __name__ == '__main__':
    init_db()
    print("服务启动: http://127.0.0.1:5000")
    app.run(debug=False, port=5000)
