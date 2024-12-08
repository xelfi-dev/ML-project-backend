from sqlalchemy import create_engine, inspect

# Replace with your actual PostgreSQL connection string
db_url = "postgresql://transactions_k7us_user:8clpBdSCNtfjzzEcGk67FsyONA1TwelP@dpg-ct8tu8btq21c739uogkg-a.oregon-postgres.render.com/transactions_k7us"

# Create an engine to connect to the database
engine = create_engine(db_url)

# Use the inspect function to get the schema information
inspector = inspect(engine)

# Get all table names
tables = inspector.get_table_names()
print("Tables in the database:")
for table in tables:
    print(table)

# Get columns for a specific table
for table in tables:
    columns = inspector.get_columns(table)
    print(f"Columns for {table}:")
    for column in columns:
        print(column['name'], column['type'])
