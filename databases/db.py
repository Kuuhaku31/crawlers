# db.py

"""
数据库表结构

create table torrents(

ID int primary key auto_increment,
type varchar(255),
title varchar(500) not null,
description text,
link varchar(255),
enclosureLink varchar(255) not null,
infoHash varchar(40) not null,
pubDate varchar(255) not null
savePath varchar(255)

);

"""

import csv
import json

import pymysql

databasename = "rsslog"
tablename = "torrents"
username = "root"
password = ""
connectdata = {"host": "localhost", "user": username, "password": password, "database": databasename, "charset": "utf8"}


# 从数据库获取数据
def get_torrent_data_that_isnt_downloaded():
    print("-" * 80)
    print("start get torrent data that isn't downloaded...")

    data_lists = []

    try:
        # 连接数据库
        conn = pymysql.connect(**connectdata)
        cursor = conn.cursor()

        # 查询所有未下载的数据的下载链接和保存路径
        sql = f"SELECT ID, enclosureLink, savePath FROM {tablename} WHERE isDownloaded = 0"
        cursor.execute(sql)
        rows = cursor.fetchall()

        for row in rows:
            data_lists.append({"ID": row[0], "enclosureLink": row[1], "savePath": row[2]})

        print("get data done")
        print(f"get {len(data_lists)} records")

    except pymysql.MySQLError as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        conn.close()

    print("=" * 80)

    return data_lists


# 修改数据
def update_data_is_downloaded(downloaded_ids):
    print("-" * 80)
    print("start update data...")

    total = 0

    if downloaded_ids is not None:
        conn = pymysql.connect(**connectdata)
        cursor = conn.cursor()

        for id in downloaded_ids:
            total += 1
            sql = f"UPDATE {tablename} SET isDownloaded=1 WHERE ID=%s"
            cursor.execute(sql, [id])
            conn.commit()

        cursor.close()
        conn.close()

    else:
        print("no data need to be updated")

    print("update done, " + str(total) + " records updated")
    print("=" * 80)


# 插入数据
def insert_data(json_path):
    print("-" * 80)
    print("start insert data...")

    with open(json_path, encoding="utf-8") as f:
        json_datas = json.load(f)
        torrent_datas = []
        for json_data in json_datas:
            torrent_datas.append(json_data["torrent_data"])

    conn = pymysql.connect(**connectdata)
    cursor = conn.cursor()

    total = 0
    success = 0
    exist = 0
    failed = 0

    for torrent_data in torrent_datas:
        total += 1

        # 如果数据已经存在，则跳过
        sql = f"SELECT * FROM {tablename} WHERE link=%s AND enclosureLink=%s"
        cursor.execute(sql, [torrent_data["link"], torrent_data["enclosureLink"]])
        if cursor.fetchone():
            exist += 1

        # 否则插入数据
        else:
            sql = f"INSERT INTO {tablename} (type, title, description, link, enclosureLink, infoHash, pubDate, savePath) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

            cursor.execute(
                sql,
                [
                    torrent_data["type"],
                    torrent_data["title"],
                    torrent_data["description"],
                    torrent_data["link"],
                    torrent_data["enclosureLink"],
                    torrent_data["infoHash"],
                    torrent_data["pubDate"],
                    torrent_data["savePath"],
                ],
            )
            conn.commit()
            success += 1
            print("insert success: " + torrent_data["title"])

    msg = f"insert done, {total} records in total, {success} records inserted, {exist} records exist, {failed} records failed"
    print(msg)

    cursor.close()
    conn.close()

    print("=" * 80)


# 导出数据到文件
def export_to_file(file_path):
    print("-" * 80)
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
    export_to_file("F:/test.csv")
    pass
