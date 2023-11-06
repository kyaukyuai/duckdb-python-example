import pandas as pd
import requests
import duckdb

# APIからデータを取得
response = requests.get('https://jsonplaceholder.typicode.com/todos')
data = response.json()
df = pd.DataFrame(data)

con = duckdb.connect(database=':memory:', read_only=False)
con.register('data', df)

con.execute('CREATE TABLE todos AS SELECT * FROM data')

result = con.execute("SELECT * FROM todos").fetchdf()

print(result)
