# db.py

"""
数据库表结构

create table mikantorrents(

id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
type varchar(2048),
pubDate varchar(2048),
title varchar(2048),
description text,
link varchar(2048),
enclosureLink varchar(2048) not null,
infoHash varchar(2048),
savePath varchar(2048),
isDownloaded bool default 0

);

"""

import csv

import pymysql

import databases.__init__ as init


# 数据库操作类
class DB:
    # 构造函数
    def __init__(self):
        self.mysql = init.mysql_config

        # 数据库连接参数
        self.host = self.mysql["host"]
        self.port = self.mysql["port"]
        self.user = self.mysql["user"]
        self.password = self.mysql["password"]
        self.charset = self.mysql["charset"]
        self.databasename = ""
        self.tablename = ""

        # 数据库链接
        self.conn = None
        self.cursor = None

    # 析构函数
    def __del__(self):
        self.close()

    # 连接数据库
    def connect(self, database):
        if self.databasename:
            print("already connected to" + self.host + "." + self.databasename)
            return

        if database in self.mysql["databases"]:
            self.databasename = database
            self.tablename = ""

            print("connecting...")
            self.conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.databasename,
                charset=self.charset,
            )
            self.cursor = self.conn.cursor()
            print(f"connected to {self.host}.{self.databasename} (port: {self.port})")

        else:
            print("database not found")

    # 设置表
    def set_tablename(self, table):
        if not table:
            self.tablename = ""
            print("table cleared")
            return

        if not self.databasename:
            print("please connect to the database first")
            return

        if table in self.mysql["databases"][self.databasename]["tables"]:
            self.tablename = table
            print("set table " + table)

        else:
            print("table not found")

    # 关闭数据库
    def close(self):
        if self.databasename:
            self.databasename = ""
            self.tablename = ""

            self.cursor.close()
            self.conn.close()

            print("disconnected from " + self.host + "." + self.databasename)

    """
    datas = [
    [
    value01,
    value02,
    ...
    ],
    [
    value01,
    value02,
    ...
    ],
    ...
    """

    # 插入数据
    def insert(self, columns, datas, check):  # check是检查是否重复的列 如[0,1,3]表示要检查第0,1,3列是否重复
        # 如果没有连接数据库，则返回
        if not self.databasename:
            print("please connect to the database first")
            return

        if not self.tablename:
            print("please set the table first")
            return

        # 如果data为空，则返回
        if columns == [] or datas == [] or check == []:
            print("column or data or check is empty")
            return

        columns_str = ",".join(columns)
        check_str = " AND ".join([f"{columns[i]}=%s" for i in check])

        print("-" * 80)
        print("start insert data where column: " + columns_str)

        total = 0
        success = 0
        exist = 0
        failed = 0
        faileds = []

        for data in datas:
            total += 1

            # 生成sql语句
            data_str = "(" + ",".join(["%s" for _ in range(len(columns))]) + ")"
            sql = f"INSERT INTO {self.tablename} ({columns_str}) VALUES {data_str};"
            sql_check = f"SELECT ID FROM {self.tablename} WHERE {check_str};"

            try:
                # 检查是否重复
                self.cursor.execute(sql_check, [data[i] for i in check])
                result = self.cursor.fetchall()
                if result:
                    exist += 1
                    continue

                self.cursor.execute(sql, data)
                self.conn.commit()
                print("insert success: " + data[2])
                success += 1

            except pymysql.MySQLError as e:
                print("insert failed: " + data[2])
                print(f"Error: {e}")
                faileds.append(data)
                failed += 1

        print(f"insert done, {total} records in total, {success} records inserted, {failed} records failed")
        print("=" * 80)

        return faileds

    # 删除数据
    def dilByID(self, ids):
        # 如果没有连接数据库，则返回
        if not self.databasename:
            print("please connect to the database first")
            return

        if not self.tablename:
            print("please set the table first")
            return

        # 如果ids为空，则返回
        if not ids:
            print("ids is empty")
            return

        # 生成sql语句
        sql = f"DELETE FROM {self.tablename} WHERE ID=%s ;"

        print("-" * 80)
        print("start delete data...")

        total = 0
        success = 0
        failed = 0
        faileds = []

        for id in ids:
            total += 1

            try:
                self.cursor.execute(sql, [id])
                self.conn.commit()
                print("delete success: " + id)
                success += 1

            except pymysql.MySQLError as e:
                print("delete failed: " + id)
                print(f"Error: {e}")
                faileds.append(id)
                failed += 1

        print(f"delete done, {total} records in total, {success} records deleted, {failed} records failed")
        print("=" * 80)

        return faileds

    # 修改数据

    def update(self, columns, datas, ids):
        # 如果没有连接数据库，则返回
        if not self.databasename:
            print("please connect to the database first")
            return

        if not self.tablename:
            print("please set the table first")
            return

        # 如果columns, datas或ids为空，则返回
        if not columns or not datas or not ids:
            print("columns, datas or ids is empty")
            return

        # 如果datas和ids不匹配，则返回
        if len(datas) != len(ids):
            print("datas and ids are not matched")
            return

        # 生成sql语句
        set_clause = ", ".join([f"{col}=%s" for col in columns])
        sql = f"UPDATE {self.tablename} SET {set_clause} WHERE ID=%s;"

        print("-" * 80)
        print("start update data where columns: " + ", ".join(columns))

        total = 0
        success = 0
        failed = 0
        faileds = []

        for id, data in zip(ids, datas):
            total += 1

            try:
                self.cursor.execute(sql, [data] + [id])
                self.conn.commit()
                print("update success: " + str(id))
                success += 1

            except pymysql.MySQLError as e:
                print("update failed: " + str(id))
                print(f"Error: {e}")
                faileds.append(id)
                failed += 1

        print(f"update done, {total} records in total, {success} records updated, {failed} records failed")
        print("=" * 80)

        return

    # 查询数据
    def select(self, columns="", condition=""):
        ids = self.selectID(condition)
        data = self.selectData(ids, columns)
        return data

    def selectID(self, condition=""):
        # 如果没有连接数据库，则返回空列表
        if not self.databasename:
            print("please connect to the database first")
            return []

        if not self.tablename:
            print("please set the table first")
            return []

        # 如果条件为空，则查询所有数据
        if condition == "":
            condition = "1=1"

        sql = f"SELECT ID FROM {self.tablename} WHERE {condition} ;"
        print("-" * 80)
        print("start select id where condition: " + condition)

        try:
            self.cursor.execute(sql)
            ids = self.cursor.fetchall()

        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            print("=" * 80)
            return []

        print(f"select done, {len(ids)} records selected")
        print("=" * 80)
        return ids

    def selectData(self, ids, column=""):
        # 如果没有连接数据库，则返回空列表
        if not self.databasename:
            print("please connect to the database first")
            return []

        if not self.tablename:
            print("please set the table first")
            return []

        # 如果ids为空，则返回空列表
        if not ids:
            print("ids is empty")
            return []

        # 如果条件为空，则查询所有数据
        if column == []:
            column = ["*"]

        # 生成sql语句
        columnstr = ",".join(column)
        sql = f"SELECT {columnstr} FROM {self.tablename} WHERE ID=%s ;"

        print("-" * 80)
        print("start select data where column: " + str(column))

        try:
            data = []
            for id in ids:
                self.cursor.execute(sql, [id])
                data.append(self.cursor.fetchone())

        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            print("=" * 80)
            return []

        print(f"select done, {len(data)} records selected")
        print("=" * 80)
        return data

    # 导出数据到文件
    def export_to_file(self, file_path, condition=""):
        # 如果没有连接数据库，则返回
        if not self.databasename:
            print("please connect to the database first")
            return

        if not self.tablename:
            print("please set the table first")
            return

        # 如果条件为空，则查询所有数据
        if condition == "":
            condition = "1=1"

        sql = f"SELECT * FROM {self.tablename} WHERE {condition};"

        print("-" * 80)
        print("start export data where sql: " + sql)

        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            headers = [i[0] for i in self.cursor.description]

            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows)

            print(f"found {len(rows)} records")
            print(f"data has been exported to {file_path}")

        except pymysql.MySQLError as e:
            print(f"Error: {e}")

        print("=" * 80)


if __name__ == "__main__":
    db = DB()
    inp = input("enter the name of the database: ")
    db.connect(inp)
    inp = input("enter the name of the table: ")
    db.set_tablename(inp)

    while True:
        inp = input("enter select condition: ")

        if inp == "q":
            break

        db.export_to_file("./ignore/data.csv", inp)

    inp = input("press any key to quit: ")
    pass
