from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Order Service is running!"})

@app.route('/orders')
def get_orders():
    orders = [
        {"id": 101, "user_id": 1, "total": 250.50},
        {"id": 102, "user_id": 2, "total": 175.25},
        {"id": 103, "user_id": 3, "total": 99.99}
    ]
    return jsonify(orders)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
