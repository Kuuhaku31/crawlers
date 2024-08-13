# Description: Python MySQL 数据库操作示例

# 导入 pymysql 模块
import pymysql

# 创建数据库
# create database dbtest default charset utf8 collate utf8_general_ci;

"""
数据库表结构

create table torrents(

title varchar(500) not null,
description text,
link varchar(255),
enclosureLink varchar(255) not null,
infoHash varchar(40) not null,
pubDate varchar(255) not null

);

"""

connect_data = {"host": "localhost", "user": "root", "password": "", "database": "dbtest", "charset": "utf8"}


# 查询缺失的 ID
def get_missing_id(cursor):
    # 查询最小的 ID
    sql = "select * from user where id=1"
    cursor.execute(sql)
    if not cursor.fetchone():
        return 13

    else:
        # 查询缺失的 ID
        sql = """
        SELECT t1.id + 1
        FROM user t1
        LEFT JOIN user t2 ON t1.id + 1 = t2.id
        WHERE t2.id IS NULL
        ORDER BY t1.id
        LIMIT 1;
        """
        cursor.execute(sql)
        result = cursor.fetchone()

        return result[0] if result is not None else None


# 用户注册
def register():
    print("用户注册")

    # 输入用户名和密码
    username = input("请输入用户名：")
    password = input("请输入密码：")

    # 连接数据库
    conn = pymysql.connect(**connect_data)
    cursor = conn.cursor()

    # 查询用户名是否存在
    sql = "select * from user where username=%s"
    cursor.execute(sql, [username])
    result = cursor.fetchone()

    if result:
        print("用户名已存在")
    else:
        # 分配 ID
        missing_id = get_missing_id(cursor)
        if missing_id:
            sql = "insert into user(id, username, password) values(%s, %s, %s)"
            cursor.execute(sql, [missing_id, username, password])
            conn.commit()

        else:
            sql = "insert into user(username, password) values(%s, %s)"
            cursor.execute(sql, [username, password])
            conn.commit()

        print("注册成功")

    # 关闭数据库1
    cursor.close()
    conn.close()


# 用户登录
def login():
    print("用户登录")

    # 输入用户名和密码
    username = input("请输入用户名：")
    password = input("请输入密码：")

    # 连接数据库
    conn = pymysql.connect(**connect_data)
    cursor = conn.cursor()

    # 查询用户名和密码是否正确
    sql = "select * from user where username=%s and password=%s"
    cursor.execute(sql, [username, password])
    result = cursor.fetchone()

    if result:
        while True:
            print("登录成功")
            print("欢迎 ", username)
            print("1. 修改数据")
            print("2. 修改密码")
            print("3. 修改用户名")
            print("4. 删除用户")
            print("q. 退出")

            choice = input("请选择：")

            if choice == "1":
                new_data = input("请输入新数据：")
                sql = "update user set data=%s where username=%s"
                cursor.execute(sql, [new_data, username])
                conn.commit()
                print("修改成功")

            elif choice == "2":
                new_password = input("请输入新密码：")
                sql = "update user set password=%s where username=%s"
                cursor.execute(sql, [new_password, username])
                conn.commit()
                print("修改成功")

            elif choice == "3":
                new_username = input("请输入新用户名：")
                sql = "update user set username=%s where username=%s"
                cursor.execute(sql, [new_username, username])
                conn.commit()
                print("修改成功")
                username = new_username

            elif choice == "4":
                confirm = input("请确认是否删除用户 " + username + " (y/n)：")

                if confirm != "y":
                    print("取消删除")
                    continue

                sql = "delete from user where username=%s"
                cursor.execute(sql, [username])
                conn.commit()
                print("删除成功")
                break

            elif choice == "q":
                print("退出成功")
                break

            else:
                print("无效选择")

    else:
        print("用户名或密码错误")

    # 关闭数据库
    cursor.close()
    conn.close()


def main():
    while True:
        print("=" * 80)
        print("用户管理系统")

        print("1. 注册")
        print("2. 登录")
        print("3. 退出")

        choice = input("请选择：")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            break
        else:
            print("无效选择")


if __name__ == "__main__":
    main()
