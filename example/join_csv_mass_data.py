import duckdb

con = duckdb.connect(database=':memory:', read_only=False)

con.execute("CREATE TABLE order_items AS SELECT * FROM read_csv_auto('./data/e-commerce/olist_order_items_dataset.csv')")
con.execute("CREATE TABLE orders AS SELECT * FROM read_csv_auto('./data/e-commerce/olist_orders_dataset.csv')")
con.execute("CREATE TABLE products AS SELECT * FROM read_csv_auto('./data/e-commerce/olist_products_dataset.csv')")

result = con.execute("""
    SELECT order_items.order_id, products.product_id, products.product_category_name, orders.order_status 
    FROM order_items 
    LEFT JOIN products ON order_items.product_id = products.product_id
    LEFT JOIN orders ON order_items.order_id = orders.order_id
""").fetchdf()

print(result)
