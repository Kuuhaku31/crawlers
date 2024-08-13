# Description: Python MySQL 数据库操作示例

# 创建数据库
# create database dbtest default charset utf8 collate utf8_general_ci;

import mysql.connector

# 创建连接
conn = mysql.connector.connect(
    host="localhost",  # 主机地址
    user="root",  # 用户名
    password="",  # 密码
    database="dbtest",  # 数据库名
)

# 创建游标对象
cursor = conn.cursor()

# 创建表
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    age INT
)
""")

# 插入数据
sql = "INSERT INTO students (name, age) VALUES (%s, %s)"
values = [("Alice", 20), ("Bob", 21), ("Charlie", 22)]
cursor.executemany(sql, values)
conn.commit()

# 查询数据
cursor.execute("SELECT * FROM students")
results = cursor.fetchall()
for row in results:
    print(row)

# 更新数据
sql = "UPDATE students SET age = %s WHERE name = %s"
cursor.execute(sql, (23, "Alice"))
conn.commit()

# 删除数据
sql = "DELETE FROM students WHERE name = %s"
cursor.execute(sql, ("Charlie",))
conn.commit()

# 关闭连接
cursor.close()
conn.close()
