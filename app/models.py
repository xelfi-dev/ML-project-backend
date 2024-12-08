from . import db


class Transaction(db.Model):
    __tablename__ = 'transactions'

    InvoiceNo = db.Column(db.String, primary_key=True)  # InvoiceNo as TEXT (Primary Key)
    StockCode = db.Column(db.String, nullable=False)  # StockCode as TEXT
    Description = db.Column(db.String, nullable=False)  # Description as TEXT
    Quantity = db.Column(db.BigInteger, nullable=False)  # Quantity as BIGINT
    InvoiceDate = db.Column(db.DateTime, nullable=False)  # InvoiceDate as TIMESTAMP
    UnitPrice = db.Column(db.Float, nullable=False)  # UnitPrice as DOUBLE PRECISION
    CustomerID = db.Column(db.BigInteger, nullable=False)  # CustomerID as BIGINT
    Country = db.Column(db.String, nullable=True)  # Country as TEXT
    TotalSpent = db.Column(db.Float, nullable=False)  # TotalSpent as DOUBLE PRECISION
    TotalSpend = db.Column(db.Float, nullable=False)  # TotalSpend as DOUBLE PRECISION

    def __repr__(self):
        return f"<Transaction {self.invoiceNo} - {self.description}>"


class Product(db.Model):
    __tablename__ = 'products'

    StockCode = db.Column(db.String, primary_key=True)  # StockCode as TEXT (Primary Key)
    Description = db.Column(db.String, nullable=False)  # Description as TEXT
    UnitPrice = db.Column(db.Float, nullable=False)  # UnitPrice as DOUBLE PRECISION

    def __repr__(self):
        return f"<Product {self.stock_code} - {self.description}>"
