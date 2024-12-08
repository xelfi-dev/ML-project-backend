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
