# 解析 XML 数据

import json
import re

from lxml import etree

import Log.save_log as sl

"""
<item>
    <title>拳奴死闘伝セスタス 第01-11巻 [Kendo Shitouden Cestvs vol 01-11]</title>
    <link>https://nyaa.land/download/1858417.torrent</link>
    <guid isPermaLink="true">https://nyaa.land/view/1858417</guid>
    <pubDate>Sun, 11 Aug 2024 13:31:38 -0000</pubDate>
    <nyaa:seeders>1</nyaa:seeders>
    <nyaa:leechers>3</nyaa:leechers>
    <nyaa:downloads>0</nyaa:downloads>
    <nyaa:infoHash>d2d3cbee40b26629af5529c1818cb21d18e514d3</nyaa:infoHash>
    <nyaa:categoryId>3_3</nyaa:categoryId>
    <nyaa:category>Literature - Raw</nyaa:category>
    <nyaa:size>1.2 GiB</nyaa:size>
    <nyaa:comments>0</nyaa:comments>
    <nyaa:trusted>No</nyaa:trusted>
    <nyaa:remake>No</nyaa:remake>
    <description>
        <![CDATA[ <a href="https://nyaa.land/view/1858417">#1858417 | 拳奴死闘伝セスタス 第01-11巻 [Kendo Shitouden Cestvs vol 01-11]</a> | 1.2 GiB | Literature - Raw | D2D3CBEE40B26629AF5529C1818CB21D18E514D3 ]]>
    </description>
</item>
"""

# 保存路径
torrent_save_file = "D:/RSS/torrent/mikan/"


# 针对 nyaa.land 的 RSS 数据解析
# 解析 XML 数据，返回字典列表
def get_data(xml, json_save_path):
    print("-" * 80)
    print("nyaa is parsing XML data...")

    root = etree.fromstring(xml)

    nyaa_items = []  # 遍历每个 <item> 元素，并存到data

    # 定义命名空间映射
    namespaces = {
        "nyaa": "https://nyaa.land/xmlns/nyaa",
        "atom": "http://www.w3.org/2005/Atom",
    }
    for item in root.xpath("//item"):
        # 用字典存储信息
        nyaa_item = {}

        # 提取基本信息
        nyaa_item["title"] = item.find("title").text if item.find("title") is not None else ""
        nyaa_item["link"] = item.find("link").text if item.find("link") is not None else ""
        nyaa_item["guid"] = item.find("guid").text if item.find("guid") is not None else ""
        nyaa_item["guid_isPermaLink"] = item.find("guid").get("isPermaLink") if item.find("guid") is not None else ""
        nyaa_item["pubDate"] = item.find("pubDate").text if item.find("pubDate") is not None else ""
        nyaa_item["nyaa:seeders"] = (
            item.find("nyaa:seeders", namespaces).text if item.find("nyaa:seeders", namespaces) is not None else ""
        )
        nyaa_item["nyaa:leechers"] = (
            item.find("nyaa:leechers", namespaces).text if item.find("nyaa:leechers", namespaces) is not None else ""
        )
        nyaa_item["nyaa:downloads"] = (
            item.find("nyaa:downloads", namespaces).text if item.find("nyaa:downloads", namespaces) is not None else ""
        )
        nyaa_item["nyaa:infoHash"] = (
            item.find("nyaa:infoHash", namespaces).text if item.find("nyaa:infoHash", namespaces) is not None else ""
        )
        nyaa_item["nyaa:categoryId"] = (
            item.find("nyaa:categoryId", namespaces).text
            if item.find("nyaa:categoryId", namespaces) is not None
            else ""
        )
        nyaa_item["nyaa:category"] = (
            item.find("nyaa:category", namespaces).text if item.find("nyaa:category", namespaces) is not None else ""
        )
        nyaa_item["nyaa:size"] = (
            item.find("nyaa:size", namespaces).text if item.find("nyaa:size", namespaces) is not None else ""
        )
        nyaa_item["nyaa:comments"] = (
            item.find("nyaa:comments", namespaces).text if item.find("nyaa:comments", namespaces) is not None else ""
        )
        nyaa_item["nyaa:trusted"] = (
            item.find("nyaa:trusted", namespaces).text if item.find("nyaa:trusted", namespaces) is not None else ""
        )
        nyaa_item["nyaa:remake"] = (
            item.find("nyaa:remake", namespaces).text if item.find("nyaa:remake", namespaces) is not None else ""
        )
        nyaa_item["description"] = item.find("description").text if item.find("description") is not None else ""

        # 打包到 torrent_datas
        torrent_data = {
            "type": "nyaa",
            "title": nyaa_item["title"],
            "description": nyaa_item["description"],
            "link": nyaa_item["link"],
            "enclosureLink": nyaa_item["link"],
            "infoHash": nyaa_item["nyaa:infoHash"],
            "pubDate": nyaa_item["pubDate"],
        }

        # 生成savePath
        part01 = f"[{torrent_data["type"]}]"
        length01 = len(part01)
        part02 = f"[{torrent_data["title"]}]"
        length02 = len(part02)
        part03 = f"[{torrent_data["pubDate"]}]"
        length03 = len(part03)

        # 限制文件名长度
        length = length01 + length02 + length03
        if length > 255:
            part02 = part02[: 255 - length01 - length03]
        file_name = part01 + part02 + part03

        # 处理文件名中的非法字符
        file_name = re.sub(r"[\/:*?\"<>|\\]", "-", file_name)

        # 保存路径
        torrent_data["savePath"] = torrent_save_file + file_name + ".torrent"

        # 添加到字典
        nyaa_item["torrent_data"] = torrent_data

        # 打包到 mikan_items
        nyaa_items.append(nyaa_item)

    # 保存到 json 文件
    with open(json_save_path, "w", encoding="utf-8") as file:
        # 清空文件
        file.truncate()
        json.dump(nyaa_items, file, ensure_ascii=False, indent=4)

    # 保存到log
    sl.log(nyaa_items)

    print("nyaa data parsed, " + str(len(nyaa_items)) + " items found")
    print("-" * 80)

    # 返回字典列表
    return nyaa_items
