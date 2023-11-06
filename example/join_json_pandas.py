import duckdb
import pandas as pd

# JSONファイルの読み込み
users_df = pd.read_json('./data/users.json')
purchases_df = pd.read_json('./data/purchases.json')

con = duckdb.connect(database=':memory:', read_only=False)

# DataFrameをDuckDBテーブルとして登録
con.register('users', users_df)
con.register('purchases', purchases_df)

# JOINクエリの実行
result = con.execute("""
    SELECT users.id, users.name, purchases.item, purchases.amount
    FROM users
    JOIN purchases ON users.id = purchases.user_id
""").fetchdf()

print(result)
