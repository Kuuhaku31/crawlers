# 下载种子文件
import os

import fake_useragent
import requests

ua = fake_useragent.UserAgent()


# 返回下载成功（或是已经下载）的ID列表
def download_torrent(data_lists):
    print("-" * 80)
    print("download start...")

    total = 0
    exist = 0
    download = 0
    download_failed = 0

    downloade_ids = []

    for data in data_lists:
        total += 1

        url = data["enclosureLink"]
        path = data["savePath"]

        # 如果文件已经存在，则跳过
        if os.path.exists(path):
            exist += 1
            downloade_ids.append(data["ID"])
            continue

        # 下载文件
        print("downloading " + path)
        try:
            res = requests.get(url, headers={"User-Agent": ua.random})
            if res.status_code == 200:
                with open(path, "wb") as f:
                    f.write(res.content)
                print("download done")
                downloade_ids.append(data["ID"])
                download += 1
            else:
                print("download failed code: " + str(res.status_code))
                download_failed += 1

        except Exception as e:
            print("download failed: " + str(e))
            download_failed += 1

    # 下载完成
    # 打印下载结果
    msg = f"download done, {total} files found, {exist} files exist, {download} files downloaded, {download_failed} files failed"
    print(msg)
    print("=" * 80)

    return downloade_ids
