# db.py

"""
数据库表结构

create table torrents(

ID int primary key auto_increment,
title varchar(500) not null,
description text,
link varchar(255),
enclosureLink varchar(255) not null,
infoHash varchar(40) not null,
pubDate varchar(255) not null

);

"""

import csv

import pymysql

databasename = "rsslog"
tablename = "torrents"
username = "root"
password = ""
connectdata = {"host": "localhost", "user": username, "password": password, "database": databasename, "charset": "utf8"}


# 插入数据
def insert_data(datas):
    print("start insert data...")

    conn = pymysql.connect(**connectdata)
    cursor = conn.cursor()

    total = 0
    success = 0
    exist = 0
    failed = 0

    for data in datas:
        total += 1

        # 拆包
        values = (
            data["title"],
            data["description"],
            data["link"],
            data["enclosureLink"],
            data["infoHash"],
            data["pubDate"],
        )

        # 如果数据已经存在，则跳过
        sql = f"SELECT * FROM {tablename} WHERE link=%s AND enclosureLink=%s"
        cursor.execute(sql, [data["link"], data["enclosureLink"]])
        if cursor.fetchone():
            exist += 1

        else:
            sql = f"INSERT INTO {tablename} (title, description, link, enclosureLink, infoHash, pubDate) VALUES (%s, %s, %s, %s, %s, %s)"

            cursor.execute(sql, values)
            conn.commit()
            success += 1
            print("insert success: " + data["title"])

    msg = f"insert done, {total} records in total, {success} records inserted, {exist} records exist, {failed} records failed"

    print(msg)
    print("=" * 80)

    cursor.close()
    conn.close()


# 导出数据到文件
def export_to_file(file_path):
    print("start export data...")

    conn = pymysql.connect(**connectdata)
    cursor = conn.cursor()

    sql = f"SELECT * FROM {tablename}"

    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        headers = [i[0] for i in cursor.description]

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

        print(f"data has been exported to {file_path}")

    except pymysql.MySQLError as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        conn.close()

    print("=" * 80)


def main():
    data = {
        "title": "ad",
        "description": "ttt",
        "link": "777",
        "enclosureLink": "777",
        "infoHash": "444",
        "pubDate": "555",
    }
    insert_data(data)


if __name__ == "__main__":
    # main()
    # export_to_file("F:/test.csv")
    pass
