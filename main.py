# main.py
# 主入口

import fake_useragent

import crawler.crawl as cl
import databases.db as db
import download.download_torrents as dt
import ignore.url as url

# 请求头
ua = fake_useragent.UserAgent()

xml_save_path = "./ignore/data.xml"
json_save_path = "./ignore/data.json"


def help():
    print("h: help")
    print("q: exit")
    print("d: download")
    ...
    return True


def quit():
    return False


def request():
    inp = input("enter the name of the rss: ")
    if inp in url.url_dic:
        cl.crawl(url.url_dic[inp]["url"], xml_save_path)
    else:
        print("rss not found")
    return True


def parse():
    inp = input("enter the name of the method: ")
    if inp in url.url_dic:
        rss_method = url.url_dic[inp]["method"]

        with open(xml_save_path, "rb") as f:
            xml = f.read()

        resualt = rss_method(xml)
        with open(json_save_path, "w") as f:
            f.write(str(resualt))

    else:
        print("method not found")


def insert():
    with open(json_save_path) as f:
        data = f.read()
        db.insert_data(data)


def download():
    dt.download_torrent()
    return True


# 命令字典
cmd_dic = {
    "h": help,  # 帮助
    "q": quit,  # 退出
    "r": request,  # 请求
    "p": parse,  # 解析
    "i": insert,  # 插入
    "d": download,  # 下载
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
        cl.crawl(rss_url)

        # 读取 RSS 数据
        with open(cl.save_path, "rb") as f:
            xml = f.read()

        # 根据不同的 RSS 网站，需要不同解析方法
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
