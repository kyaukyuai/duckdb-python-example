from dotenv import load_dotenv
import os
import duckdb

load_dotenv()

s3_endpoint = os.getenv("S3_ENDPOINT")
s3_access_key_id = os.getenv("S3_ACCESS_KEY_ID")
s3_secret_access_key = os.getenv("S3_SECRET_ACCESS_KEY")
bucket_name = os.getenv("BUCKET_NAME")

con = duckdb.connect(database=':memory:', read_only=False)

con.install_extension("httpfs")
con.load_extension("httpfs")

con.execute(f"SET s3_endpoint='{s3_endpoint}'")
con.execute(f"SET s3_access_key_id='{s3_access_key_id}'")
con.execute(f"SET s3_secret_access_key='{s3_secret_access_key}'")

con.execute(f"""
    CREATE TABLE order_items AS
    SELECT * FROM read_csv_auto('s3://{bucket_name}/olist_order_items_dataset.csv')
""")
con.execute(f"""
    CREATE TABLE orders AS
    SELECT * FROM read_csv_auto('s3://{bucket_name}/olist_orders_dataset.csv')
""")
con.execute(f"""
    CREATE TABLE products AS
    SELECT * FROM read_csv_auto('s3://{bucket_name}/olist_products_dataset.csv')
""")

result = con.execute(f"""
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
