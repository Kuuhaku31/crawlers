# 下载种子文件
import os
import re

import fake_useragent
import requests

ua = fake_useragent.UserAgent()


def download_torrent(data_list, path):
    # 如果文件夹不存在，则创建
    if not os.path.exists(path):
        os.makedirs(path)

    print("download start...")

    download = 0
    download_failed = 0

    for data in data_list:
        # 文件名（去除特殊字符）
        file_title = data["torrent_name"]

        # title 太长时截取
        if len(file_title) > 150:
            file_title = file_title[:150]

        file_name = file_title + " pub_date - " + data["torrent_pub_date"] + ".torrent"
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

    # 打印下载结果
    msg = f"download done, {len(data_list)} files found, {download} files downloaded, {download_failed} files failed"

    print(msg)
    print("=" * 80)
