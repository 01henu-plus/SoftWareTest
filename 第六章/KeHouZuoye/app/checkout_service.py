"""
Checkout 微服务
提供购物车结算功能的 Flask 微服务
"""
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/checkout", methods=["POST"])
def checkout():
    """
    结算接口
    
    请求格式:
    {
        "items": [
            {"price": 20, "quantity": 3},
            {"price": 15, "quantity": 2}
        ]
    }
    
    返回格式:
    成功: {"total": 60, "status": "ok"}
    失败: {"error": "empty cart"}
    """
    data = request.get_json()
    items = data.get("items", [])
    
    # 检查购物车是否为空
    if not items:
        return jsonify({"error": "empty cart"}), 400
    
    # 计算总价
    total = sum([i["price"] * i["quantity"] for i in items])
    
    return jsonify({"total": total, "status": "ok"}), 200


if __name__ == "__main__":
    print("=" * 60)
    print("  Checkout 微服务")
    print("=" * 60)
    print("\n🌐 服务地址: http://127.0.0.1:5000")
    print("📍 结算接口: POST /checkout")
    print("\n示例请求:")
    print('  POST http://127.0.0.1:5000/checkout')
    print('  Body: {"items": [{"price": 20, "quantity": 3}]}')
    print("\n按 Ctrl+C 停止服务\n")
    
    app.run(port=5000, debug=False)
