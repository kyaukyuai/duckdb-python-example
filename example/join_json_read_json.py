import duckdb

con = duckdb.connect(database=':memory:', read_only=False)

# read_jsonを使用してJSONファイルから直接データを読み込む
con.execute("CREATE TABLE users AS SELECT * FROM read_json_auto('./data/users.json')")
con.execute("CREATE TABLE purchases AS SELECT * FROM read_json_auto('./data/purchases.json')")

# JOINクエリの実行
result = con.execute("""
    SELECT users.id, users.name, purchases.item, purchases.amount
    FROM users
    JOIN purchases ON users.id = purchases.user_id
""").fetchdf()

print(result)
