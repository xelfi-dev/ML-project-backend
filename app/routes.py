from flask import Blueprint, request, jsonify
from datetime import datetime
import random
from . import db
from .models import Transaction, Product
from .utils import calculate_rfm

main_bp = Blueprint('main', __name__)


@main_bp.route('/add_products', methods=['POST'])
def add_products():
    data = request.json  # Expecting a list of products in the request body
    try:
        if not isinstance(data, list):
            return jsonify({"error": "Invalid data format. Expected a list of products."}), 400

        transactions = []  # To store all the new transaction records
        for product_data in data:
            # Generate a new invoice number if not provided
            if 'invoiceNo' not in product_data:
                invoice_no = f"{random.randint(100000, 999999)}"
            else:
                invoice_no = product_data['invoiceNo']

            # Generate a new customer ID if not provided
            if 'customerId' not in product_data:
                customer_id = f"{random.randint(10000, 99999)}"  # Generate a random 5-digit customer ID
            else:
                customer_id = product_data['customerId']

            # Fetch product details from the products table using the description
            product = Product.query.filter_by(Description=product_data['description']).first()

            if not product:
                return jsonify(
                    {"error": f"Product '{product_data['description']}' not found in the products table"}), 404

            # Create a new transaction record
            new_transaction = Transaction(
                InvoiceNo=invoice_no,
                StockCode=product.StockCode,
                Description=product.Description,
                Quantity=int(product_data['quantity']),
                InvoiceDate=datetime.strptime(product_data['date'], '%Y-%m-%d'),
                # Assuming 'date' is in 'YYYY-MM-DD' format
                UnitPrice=product.UnitPrice,
                CustomerID=customer_id,
                Country=product_data['country'],
                TotalSpent=product.UnitPrice * int(product_data['quantity']),
                TotalSpend=product.UnitPrice * int(product_data['quantity'])
            )

            transactions.append(new_transaction)

        # Add all new transactions to the database in a single commit
        db.session.bulk_save_objects(transactions)
        db.session.commit()

        return jsonify({"message": f"{len(transactions)} product transactions inserted successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@main_bp.route('/get_rfm/<customer_id>', methods=['GET'])
def get_rfm(customer_id):
    try:
        # Get RFM values for the customer
        rfm = calculate_rfm(customer_id)

        if rfm:
            return jsonify(rfm), 200
        else:
            return jsonify({"error": "No data found for this customer"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# New endpoint to get a list of item descriptions
@main_bp.route('/get_items', methods=['GET'])
def get_items():
    try:
        # Query all product descriptions from the Product table
        products = Product.query.all()

        # Create a list of product descriptions
        product_descriptions = [product.Description for product in products]

        return jsonify({"items": product_descriptions}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
