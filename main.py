# main.py
# 主入口

import fake_useragent
import requests

import databases.db as db
import download.download_torrents as dt
import ignore.url as url

# 请求头
ua = fake_useragent.UserAgent()
resualt = None


def exit():
    return False


# 命令字典
cmd_dic = {
    "q": exit,
}


def update():
    cmd = input(">> ")
    if cmd in cmd_dic:
        return cmd_dic[cmd]
    else:
        print("this command is not found")
        return True


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
        # 根据不同的 RSS 网站，需要不同解析方法
        print("getting response...")
        xml = requests.get(rss_url, headers={"User-Agent": ua.random}).content
        list = rss_method(xml)

        # 下载种子文件
        dt.download_torrent(list["torrent_data"], torrent_download_path)

        # 录入数据库
        db.insert_data(list["data_list"])

        # 导出数据到文件
        db.export_to_file(data_saveing_path + "/data.csv")

    else:
        print("rss not found")

    input("press any key to exit...")


if __name__ == "__main__":
    main()
