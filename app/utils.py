from datetime import datetime
import pandas as pd
from . import db
from sqlalchemy import text


def calculate_rfm(customer_id):
    try:
        # Get all transactions for the given customer_id
        transactions = db.session.execute(
            text("SELECT * FROM transactions WHERE \"CustomerID\" = :customer_id"),
            {'customer_id': customer_id}
        ).fetchall()

        if not transactions:
            return None  # If no transactions are found for the customer

        # Convert the transactions to a DataFrame
        data = pd.DataFrame([{
            'invoice_date': t.InvoiceDate,
            'quantity': t.Quantity,
            'unit_price': t.UnitPrice
        } for t in transactions])

        # Calculate recency (days since last purchase)
        latest_date = datetime.strptime("2011-12-09", "%Y-%m-%d")  # Set fixed latest date
        recency = (latest_date - data['invoice_date'].max()).days

        # Calculate frequency (number of transactions)
        frequency = len(data)

        # Calculate monetary (total amount spent)
        data['total_spent'] = data['quantity'] * data['unit_price']
        monetary = data['total_spent'].sum()

        # Return the RFM values as a dictionary
        rfm = {
            'Recency': recency + 1,
            'Frequency': frequency,
            'Monetary': monetary
        }

        return rfm

    except Exception as e:
        return {"error": str(e)}


def recommend_products(model, user_id, top_n=3):
    try:
        # Get all unique product IDs from the Product table
        all_items = db.session.execute(
            text("SELECT \"StockCode\" FROM products")
        ).fetchall()
        all_items = [item.StockCode for item in all_items]

        # Get all items the user has already interacted with
        user_rated_items = db.session.execute(
            text("SELECT \"StockCode\" FROM transactions WHERE \"CustomerID\" = :user_id"),
            {'user_id': user_id}
        ).fetchall()
        user_rated_items = [item.StockCode for item in user_rated_items]

        # Filter items not yet interacted with by the user
        items_to_predict = [item for item in all_items if item not in user_rated_items]

        # Predict ratings for each item the user hasn't interacted with
        predictions = [model.predict(user_id, item) for item in items_to_predict]

        # Sort predictions by estimated rating in descending order
        predictions = sorted(predictions, key=lambda x: x.est, reverse=True)

        # Get the top N predictions
        top_predictions = predictions[:top_n]

        # Get product descriptions for the recommended items
        recommended_products = []
        for pred in top_predictions:
            product = db.session.execute(
                text("SELECT \"Description\" FROM products WHERE \"StockCode\" = :stock_code"),
                {'stock_code': pred.iid}
            ).fetchone()
            if product:
                recommended_products.append(product.Description)

        return recommended_products

    except Exception as e:
        return {"error": str(e)}
