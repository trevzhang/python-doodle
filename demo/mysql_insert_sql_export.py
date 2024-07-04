import pymysql
import sys
import re

# 读取命令行输入的SELECT语句
if len(sys.argv) < 2:
    print("Usage: python mysql_insert_sql_export.py '<SELECT statement>'")
    sys.exit(1)

select_statement = sys.argv[1]

# 使用正则表达式从SELECT语句中提取表名
table_name_search = re.search(r"from\s+([a-zA-Z0-9_]+)", select_statement, re.IGNORECASE)
if not table_name_search:
    print("Table name could not be extracted from the SELECT statement.")
    sys.exit(1)

table_name = table_name_search.group(1)

# 连接MySQL数据库
conn = pymysql.connect(host='10.150.19.28', port=3322, user='sdk', password='RhYcjiT1uSUsvn4MxQadwto6B8mqIgEb', db='sdk')
cursor = conn.cursor()

# 获取列名（排除id列）
cursor.execute(f"SHOW COLUMNS FROM {table_name};")
columns_info = cursor.fetchall()
columns = [col[0] for col in columns_info if col[0].lower() != 'id']
id_column_index = next((index for index, col in enumerate(columns_info) if col[0].lower() == 'id'), None)

# 动态替换查询语句中的表名并执行查询
cursor.execute(select_statement)

# 获取查询结果
rows = cursor.fetchall()

# 构造INSERT语句，包括列名但不包括id列，并动态替换表名
insert_statements = []
for row in rows:
    # 如果存在id列，从每行数据中去除id列的值
    if id_column_index is not None:
        row = row[:id_column_index] + row[id_column_index+1:]
    values = "', '".join(map(str, row))
    columns_formatted = ", ".join(columns)  # 格式化列名
    insert_statements.append(f"INSERT INTO {table_name} ({columns_formatted}) VALUES ('{values}');")

# 将INSERT语句导出到文件
with open('/tmp/insert.sql', 'w') as f:
    f.write('\n'.join(insert_statements))

# 关闭连接
cursor.close()
conn.close()