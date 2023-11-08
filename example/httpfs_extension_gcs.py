from dotenv import load_dotenv
import os
import duckdb
from duckdb import DuckDBPyConnection

REQUIRED_VARS = [
    "S3_ENDPOINT",
    "S3_ACCESS_KEY_ID",
    "S3_SECRET_ACCESS_KEY",
    "BUCKET_NAME",
]


def load_env_vars(required_vars: list[str] = REQUIRED_VARS):
    # Load .env file
    load_dotenv()
    for var in required_vars:
        if not os.getenv(var):
            raise Exception(f"Required environment variable not set: {var}")


def setup_ddb_connection() -> DuckDBPyConnection:
    conn = duckdb.connect(database=':memory:', read_only=False)

    conn.sql("INSTALL httpfs;")
    conn.sql("LOAD httpfs;")

    conn.sql(f"SET s3_endpoint='{os.getenv('S3_ENDPOINT')}'")
    conn.sql(f"SET s3_access_key_id='{os.getenv('S3_ACCESS_KEY_ID')}'")
    conn.sql(f"SET s3_secret_access_key='{os.getenv('S3_SECRET_ACCESS_KEY')}'")

    return conn


def main():
    load_env_vars()
    conn = setup_ddb_connection()

    bucket_name = os.getenv("BUCKET_NAME")

    conn.execute(f"""
        CREATE TABLE order_items AS
        SELECT * FROM read_csv_auto('s3://{bucket_name}/olist_order_items_dataset.csv')
    """)
    conn.execute(f"""
        CREATE TABLE orders AS
        SELECT * FROM read_csv_auto('s3://{bucket_name}/olist_orders_dataset.csv')
    """)
    conn.execute(f"""
        CREATE TABLE products AS
        SELECT * FROM read_csv_auto('s3://{bucket_name}/olist_products_dataset.csv')
    """)

    conn.execute(f"""
        COPY 
        ( SELECT
            order_items.order_id,
            products.product_id,
            products.product_category_name,
            orders.order_status,
            date_part('year', orders.order_estimated_delivery_date) 
        FROM order_items 
        LEFT JOIN products ON order_items.product_id = products.product_id
        LEFT JOIN orders ON order_items.order_id = orders.order_id
        ) TO 's3://{bucket_name}/output.csv' (HEADER, DELIMITER ',', QUOTE '"');
    """)


if __name__ == "__main__":
    main()
