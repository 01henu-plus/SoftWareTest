"""
Flask 订单系统 - 用于容错性和可靠性测试
支持数据库连接和订单处理
"""
from flask import Flask, request, jsonify
import sqlite3
import os
import time

app = Flask(__name__)

# 数据库文件路径
DB_FILE = 'orders.db'

def init_db():
    """初始化数据库"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # 创建订单表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL,
                qty INTEGER NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建库存表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                item TEXT PRIMARY KEY,
                stock INTEGER NOT NULL
            )
        ''')
        
        # 初始化库存
        cursor.execute("DELETE FROM inventory")
        cursor.execute("INSERT OR REPLACE INTO inventory (item, stock) VALUES ('book', 100)")
        cursor.execute("INSERT OR REPLACE INTO inventory (item, stock) VALUES ('pen', 200)")
        cursor.execute("INSERT OR REPLACE INTO inventory (item, stock) VALUES ('notebook', 150)")
        
        conn.commit()
        conn.close()
        print("✓ 数据库初始化成功")
        return True
    except Exception as e:
        print(f"✗ 数据库初始化失败: {e}")
        return False

@app.route('/')
def index():
    """主页"""
    return '''
    <h1>订单系统 - 容错性测试</h1>
    <h2>API 接口:</h2>
    <ul>
        <li>POST /order - 创建订单</li>
        <li>GET /orders - 查看所有订单</li>
        <li>GET /inventory - 查看库存</li>
        <li>GET /health - 健康检查</li>
    </ul>
    <h3>创建订单示例:</h3>
    <pre>
    POST /order
    {
        "item": "book",
        "qty": 1
    }
    </pre>
    '''

@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    try:
        conn = sqlite3.connect(DB_FILE, timeout=2)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        return jsonify({
            "status": "healthy",
            "database": "connected"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }), 503

@app.route('/order', methods=['POST'])
def create_order():
    """创建订单"""
    try:
        data = request.get_json()
        item = data.get('item', '')
        qty = data.get('qty', 0)
        
        if not item or qty <= 0:
            return jsonify({
                "status": "error",
                "message": "Invalid item or quantity"
            }), 400
        
        # 连接数据库（设置超时）
        conn = sqlite3.connect(DB_FILE, timeout=5)
        cursor = conn.cursor()
        
        # 检查库存
        cursor.execute("SELECT stock FROM inventory WHERE item=?", (item,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return jsonify({
                "status": "error",
                "message": "Item not found"
            }), 400
        
        stock = result[0]
        if stock < qty:
            conn.close()
            return jsonify({
                "status": "error",
                "message": "Insufficient stock"
            }), 400
        
        # 创建订单
        cursor.execute(
            "INSERT INTO orders (item, qty, status) VALUES (?, ?, ?)",
            (item, qty, 'completed')
        )
        order_id = cursor.lastrowid
        
        # 更新库存
        cursor.execute(
            "UPDATE inventory SET stock = stock - ? WHERE item = ?",
            (qty, item)
        )
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "status": "success",
            "message": "Order created",
            "order_id": order_id,
            "item": item,
            "qty": qty
        }), 200
        
    except sqlite3.OperationalError as e:
        # 数据库连接错误
        return jsonify({
            "status": "error",
            "message": "Database connection failed",
            "error": str(e)
        }), 503
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/orders', methods=['GET'])
def get_orders():
    """获取所有订单"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders ORDER BY id DESC LIMIT 10")
        orders = cursor.fetchall()
        conn.close()
        
        return jsonify({
            "status": "success",
            "orders": [
                {
                    "id": o[0],
                    "item": o[1],
                    "qty": o[2],
                    "status": o[3],
                    "created_at": o[4]
                } for o in orders
            ]
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/inventory', methods=['GET'])
def get_inventory():
    """获取库存"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory")
        items = cursor.fetchall()
        conn.close()
        
        return jsonify({
            "status": "success",
            "inventory": [{"item": i[0], "stock": i[1]} for i in items]
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("  订单系统 - 容错性和可靠性测试")
    print("=" * 60)
    
    # 初始化数据库
    if init_db():
        print(f"\n🌐 服务地址: http://127.0.0.1:5000")
        print(f"📊 健康检查: GET http://127.0.0.1:5000/health")
        print(f"📦 创建订单: POST http://127.0.0.1:5000/order")
        print(f"\n按 Ctrl+C 停止服务器\n")
        
        app.run(debug=True, port=5000)
    else:
        print("\n✗ 服务启动失败：数据库初始化失败")
