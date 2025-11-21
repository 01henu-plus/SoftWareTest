"""
订单系统 - 集成测试案例
包含：下单模块 + 库存模块 + 支付模块
"""
from flask import Flask, request, jsonify

app = Flask(__name__)

# 模拟库存
inventory = {"book": 10, "pen": 20, "notebook": 15}

# 模拟用户余额
user_balance = {"user1": 1000, "user2": 500}


# 库存模块
class InventoryModule:
    """库存模块"""
    
    @staticmethod
    def check_stock(item, qty):
        """检查库存"""
        if item not in inventory:
            return False, "商品不存在"
        if inventory[item] < qty:
            return False, "库存不足"
        return True, "库存充足"
    
    @staticmethod
    def reduce_stock(item, qty):
        """减少库存"""
        inventory[item] -= qty
        return inventory[item]


# 支付模块
class PaymentModule:
    """支付模块"""
    
    @staticmethod
    def check_balance(user, amount):
        """检查余额"""
        if user not in user_balance:
            return False, "用户不存在"
        if user_balance[user] < amount:
            return False, "余额不足"
        return True, "余额充足"
    
    @staticmethod
    def deduct_balance(user, amount):
        """扣除余额"""
        user_balance[user] -= amount
        return user_balance[user]


# 下单模块
@app.route("/order", methods=["POST"])
def order():
    """下单接口"""
    item = request.json.get("item")
    qty = request.json.get("qty", 1)
    user = request.json.get("user", "user1")
    price = request.json.get("price", 10)
    
    # 1. 检查库存
    stock_ok, stock_msg = InventoryModule.check_stock(item, qty)
    if not stock_ok:
        return jsonify({"error": stock_msg}), 400
    
    # 2. 检查余额
    total_amount = price * qty
    balance_ok, balance_msg = PaymentModule.check_balance(user, total_amount)
    if not balance_ok:
        return jsonify({"error": balance_msg}), 400
    
    # 3. 扣除库存
    remaining_stock = InventoryModule.reduce_stock(item, qty)
    
    # 4. 扣除余额
    remaining_balance = PaymentModule.deduct_balance(user, total_amount)
    
    return jsonify({
        "success": True,
        "剩余库存": remaining_stock,
        "剩余余额": remaining_balance
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)

