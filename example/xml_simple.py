import duckdb
import pandas as pd
import xml.etree.ElementTree as ET

# XMLデータ
# <users>
#     <user id="1" name="Alice">
#         <orders>
#             <order item="Book" amount="3"/>
#             <order item="Pen" amount="10"/>
#         </orders>
#     </user>
#     <user id="2" name="Bob">
#         <orders>
#             <order item="Bottle" amount="1"/>
#         </orders>
#     </user>
# </users>

# XMLを解析
tree = ET.parse('./data/complex_data.xml')
root = tree.getroot()

data = []

# userタグごとに情報を抽出
for user in root.findall('user'):
    user_id = user.get('id')
    user_name = user.get('name')

    # 各orderタグの情報を抽出
    for order in user.find('orders').findall('order'):
        order_item = order.get('item')
        order_amount = order.get('amount')
        data.append({'id': user_id, 'name': user_name, 'item': order_item, 'amount': order_amount})

df = pd.DataFrame(data)

con = duckdb.connect(database=':memory:', read_only=False)

con.register('xml_table', df)

result = con.execute("SELECT * FROM xml_table").fetchdf()

print(result)
