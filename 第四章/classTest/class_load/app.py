"""
订单系统 - 用于负载测试
"""
from flask import Flask, request, jsonify

app = Flask(__name__)

# 模拟库存（大量库存用于负载测试）
inventory = {"book": 100000}


@app.route("/order", methods=["POST"])
def order():
    """下单接口"""
    item = request.json.get("item")
    qty = request.json.get("qty", 1)
    
    if item not in inventory:
        return jsonify({"error": "商品不存在"}), 400
    
    if inventory[item] < qty:
        return jsonify({"error": "库存不足"}), 400
    
    inventory[item] -= qty
    return jsonify({"success": True, "remaining": inventory[item]}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8089, debug=False)

