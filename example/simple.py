import duckdb

con = duckdb.connect(database=':memory:', read_only=False)

con.execute("CREATE TABLE items (id INTEGER, name VARCHAR)")
con.execute("INSERT INTO items VALUES (1, 'Item 1'), (2, 'Item 2')")
result = con.execute("SELECT * FROM items").fetchall()

print(result)
