# rss
# 利用爬虫获取RSS订阅的内容
# 以mikanani.me的RSS为例

from datetime import datetime
import os
import re
import fake_useragent
import requests
from lxml import etree


# 资源文件地址
rss_data_path = "D:/RSS/data"
rss_torrent_path = "D:/RSS/torrent"


# RSS地址
with open("./ignore/url.txt", "r") as f:
    rss_url = f.readline().strip()

# 时间
date = ""

# 请求头
ua = fake_useragent.UserAgent()


# 解析 XML 数据
def get_data(xml_data):
    # 解析 XML 数据
    root = etree.fromstring(xml_data)

    data_list = []  # 遍历每个 <item> 元素，并存到data
    namespaces = {"ns": "https://mikanani.me/0.1/"}  # 定义命名空间映射
    for item in root.xpath("//item"):

        # 用字典存储信息
        dic = {}

        # 提取基本信息
        dic["guid"] = item.find("guid").text if item.find("guid") is not None else ""
        dic["guid_isPermaLink"] = (
            item.find("guid").get("isPermaLink")
            if item.find("guid") is not None
            else "None"
        )
        dic["link"] = item.find("link").text if item.find("link") is not None else ""
        dic["title"] = item.find("title").text if item.find("title") is not None else ""
        dic["description"] = (
            item.find("description").text
            if item.find("description") is not None
            else "None"
        )

        # 提取 <torrent> 内的信息，需要处理命名空间
        torrent_element = item.find("ns:torrent", namespaces)
        if torrent_element is not None:
            dic["torrent_link"] = (
                torrent_element.find("ns:link", namespaces).text
                if torrent_element.find("ns:link", namespaces) is not None
                else "None"
            )
            dic["content_length"] = (
                torrent_element.find("ns:contentLength", namespaces).text
                if torrent_element.find("ns:contentLength", namespaces) is not None
                else "None"
            )
            dic["pub_date"] = (
                torrent_element.find("ns:pubDate", namespaces).text
                if torrent_element.find("ns:pubDate", namespaces) is not None
                else "None"
            )

        # 提取 <enclosure> 的属性
        enclosure = item.find("enclosure")
        if enclosure is not None:
            dic["enclosure_type"] = enclosure.get("type", "")
            dic["enclosure_length"] = enclosure.get("length", "")
            dic["enclosure_url"] = enclosure.get("url", "")
        else:
            dic["enclosure_type"] = "None"
            dic["enclosure_length"] = "None"
            dic["enclosure_url"] = "None"

        # 存储到data_list
        data_list.append(dic)

    # 返回数据
    return data_list


# 保存数据
def save_data(data_list):
    save_path = rss_data_path + "/" + date + ".txt"
    print("saving data to " + save_path + "...")
    with open(save_path, "w", encoding="utf-8") as f:
        for data in data_list:
            for key in data:
                f.write(key + ": " + data[key] + "\n")
            f.write("-" * 80 + "\n")


# 下载种子文件
def download_torrent(data_list):

    download = 0
    download_failed = 0

    for data in data_list:
        if data["torrent_link"] != "None":

            # 文件名（去除特殊字符）
            file_name = data["title"] + " pub_date - " + data["pub_date"] + ".torrent"
            file_name = re.sub(r"[\/:*?\"<>|]", "-", file_name)
            download_file = rss_torrent_path + "/" + file_name

            print("for " + file_name + "...")

            # 如果文件已经存在，则跳过
            if os.path.exists(download_file):
                print("file exists, skip")
                continue

            # 下载文件
            print("downloading...")
            res = requests.get(data["enclosure_url"], headers={"User-Agent": ua.random})
            if res.status_code == 200:
                with open(download_file, "wb") as f:
                    f.write(res.content)
                print("download done")
                download += 1
            else:
                print("download failed")
                download_failed += 1

    print(
        "download done, "
        + str(len(data_list))
        + " files found, "
        + str(download)
        + " files downloaded, "
        + str(download_failed)
        + " files failed"
    )


def main():

    # 获取时间
    global date
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    print(date)

    # 获取数据
    print("getting response...")
    res = requests.get(rss_url, headers={"User-Agent": ua.random})
    print("get response done")

    # 解析数据
    data_list = get_data(res.content)

    # 保存数据
    save_data(data_list)

    # 下载种子文件
    download_torrent(data_list)

    print("done")


if __name__ == "__main__":
    main()
