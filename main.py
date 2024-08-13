# main.py
# 主入口
import os
import re
from datetime import datetime

import fake_useragent
import requests

import ignore.url as url
import Log.save_log as save_log

# 请求头
ua = fake_useragent.UserAgent()


# 保存数据
def save_data(data_list, path):
    # 如果文件夹不存在，则创建
    if not os.path.exists(path):
        os.makedirs(path)

    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_path = path + "/" + date + ".txt"

    print("saving data to " + save_path + "...")

    with open(save_path, "w", encoding="utf-8") as f:
        for data in data_list:
            for key in data:
                f.write(key + ": " + data[key] + "\n")
            f.write("-" * 80 + "\n")


# 下载种子文件
def download_torrent(data_list, path):
    # 如果文件夹不存在，则创建
    if not os.path.exists(path):
        os.makedirs(path)

    print("download start...")

    download = 0
    download_failed = 0

    for data in data_list:
        # 文件名（去除特殊字符）
        file_name = data["torrent_name"] + " pub_date - " + data["torrent_pub_date"] + ".torrent"
        file_name = re.sub(r"[\/:*?\"<>|\\]", "-", file_name)
        download_file = path + "/" + file_name

        # 如果文件已经存在，则跳过
        if os.path.exists(download_file):
            continue

        # 下载文件
        print("downloading " + file_name)
        res = requests.get(data["torrent_link"], headers={"User-Agent": ua.random})
        if res.status_code == 200:
            with open(download_file, "wb") as f:
                f.write(res.content)
            print("download done")
            download += 1
        else:
            print("download failed code: " + str(res.status_code))
            download_failed += 1

    # 下载完成
    print(
        "download done, "
        + str(len(data_list))
        + " files found, "
        + str(download)
        + " files downloaded, "
        + str(download_failed)
        + " files failed"
    )


# 入口程序
def main():
    name = input("enter the name of the rss: ")
    if name in url.url_dic:
        print("crawler start")

        # 获取 RSS 地址和解析方法
        print("getting rss data...")
        rss_url = url.url_dic[name]["url"]
        rss_method = url.url_dic[name]["method"]
        data_saveing_path = url.url_dic[name]["save_path"]
        torrent_download_path = url.url_dic[name]["download_path"]

        # 获取 RSS 数据
        print("getting response...")
        xml = requests.get(rss_url, headers={"User-Agent": ua.random}).content
        list = rss_method(xml)

        # 储存 RSS 数据
        save_data(list["data_list"], data_saveing_path)
        save_log.save_log(list["data_list"])
        # save_log.save_log_xml(xml)

        # 下载种子文件
        download_torrent(list["torrent_data"], torrent_download_path)

    else:
        print("rss not found")

    input("press any key to exit...")


if __name__ == "__main__":
    main()
