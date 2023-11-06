import duckdb

con = duckdb.connect(database=':memory:', read_only=False)

# httpfs 拡張機能をインストールしてロードする
con.install_extension("httpfs")
con.load_extension("httpfs")

result = con.execute("SELECT * FROM read_json_auto('https://jsonplaceholder.typicode.com/todos')").fetchdf()

print(result)
