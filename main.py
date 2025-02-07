from flask import Flask, request, jsonify
import requests
import math
import logging

app = Flask(__name__)

# Enable CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    return response

# Helper functions
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n < 2:
        return False
    divisors = [i for i in range(1, n // 2 + 1) if n % i == 0]
    return sum(divisors) == n

def is_armstrong(n):
    if n < 0:
        return False
    digits = [int(d) for d in str(n)]
    length = len(digits)
    return n == sum(d ** length for d in digits)

def digit_sum(n):
    return sum(int(d) for d in str(abs(n)))  # Handle negative numbers

def get_fun_fact(n):
    url = f"http://numbersapi.com/{n}/math"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text
    except requests.RequestException as e:
        logging.error(f"Error fetching fun fact: {e}")
    return "No fun fact available."

# API endpoint
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')
    
    # Input validation
    if number is None:
        return jsonify({"error": "No number provided", "number": None}), 400

    try:
        # Allow negative and floating-point numbers
        number = float(number)
        if abs(number) > 10**10:
            raise ValueError("Number out of bounds.")
    except ValueError:
        logging.error(f"Invalid input: {number}")
        return jsonify({"error": "Invalid input", "number": number}), 400

    # Convert to integer for classification (if needed)
    int_number = int(number)

    # Determine properties
    properties = []
    if is_armstrong(int_number):
        properties.append("armstrong")
    if int_number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    
    # Prepare response
    response = {
        "number": number,  # Return the original number (including floating-point)
        "is_prime": is_prime(int_number),
        "is_perfect": is_perfect(int_number),
        "properties": properties,
        "digit_sum": digit_sum(int_number),
        "fun_fact": get_fun_fact(int_number)
    }
    
    return jsonify(response), 200

# To Run the app
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
