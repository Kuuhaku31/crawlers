# 解析 XML 数据

import json

from lxml import etree

"""
数据库表结构

create table torrents(

ID                      int primary key auto_increment,
title                   varchar(500) not null,
description             text,
link                    varchar(255),
enclosureLink           varchar(255) not null,
infoHash                varchar(40) not null,
pubDate                 varchar(255) not null
savePath                varchar(255)

);

"""


# 解析 XML 数据，返回字典列表
def get_data(xml, json_save_path):
    root = etree.fromstring(xml)

    mikan_items = []

    namespaces = {"ns": "https://mikanani.me/0.1/"}  # 定义命名空间映射

    # 遍历每个 <item> 元素
    for item in root.xpath("//item"):
        # 用字典存储一个item的所有信息
        mikan_item = {}

        # 提取基本信息
        mikan_item["guid"] = item.find("guid").text if item.find("guid") is not None else ""
        mikan_item["guid_isPermaLink"] = item.find("guid").get("isPermaLink") if item.find("guid") is not None else ""
        mikan_item["link"] = item.find("link").text if item.find("link") is not None else ""
        mikan_item["title"] = item.find("title").text if item.find("title") is not None else ""
        mikan_item["description"] = item.find("description").text if item.find("description") is not None else ""

        # 提取 <torrent> 内的信息，需要处理命名空间
        torrent_element = item.find("ns:torrent", namespaces)
        if torrent_element is not None:
            mikan_item["torrent_link"] = (
                torrent_element.find("ns:link", namespaces).text
                if torrent_element.find("ns:link", namespaces) is not None
                else ""
            )
            mikan_item["torrent_contentLength"] = (
                torrent_element.find("ns:contentLength", namespaces).text
                if torrent_element.find("ns:contentLength", namespaces) is not None
                else ""
            )
            mikan_item["torrent_pubDate"] = (
                torrent_element.find("ns:pubDate", namespaces).text
                if torrent_element.find("ns:pubDate", namespaces) is not None
                else ""
            )

        # 提取 <enclosure> 的属性
        enclosure = item.find("enclosure")
        if enclosure is not None:
            mikan_item["enclosure_type"] = enclosure.get("type", "")
            mikan_item["enclosure_length"] = enclosure.get("length", "")
            mikan_item["enclosure_url"] = enclosure.get("url", "")
        else:
            mikan_item["enclosure_type"] = ""
            mikan_item["enclosure_length"] = ""
            mikan_item["enclosure_url"] = ""

        # 打包到 torrent_datas
        torrent_data = {
            "title": mikan_item["title"],
            "enclosureLink": mikan_item["enclosure_url"],
            "pubDate": mikan_item["torrent_pubDate"],
        }

        mikan_item["torrent_data"] = torrent_data

        # 打包到 mikan_items
        mikan_items.append(mikan_item)

    # 保存到 json 文件
    with open(json_save_path, "w", encoding="utf-8") as file:
        json.dump(mikan_items, file, ensure_ascii=False, indent=4)
