# main.py
# 主入口

import crawler.crawl as cl
import databases.db as db
import download.download_torrents as dt
import ignore.url as url

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
        parse_method = url.url_dic[inp]["method"]

        with open(xml_save_path, "rb") as f:
            parse_method(f.read(), json_save_path)

    else:
        print("method not found")

    return True


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
        return cmd_dic[cmd]()
    else:
        print("this command is not found")
        return True


# 入口程序
def main():
    print("welcome to the main program")
    print("type h for help")

    while update():
        pass

    input("press any key to exit...")


if __name__ == "__main__":
    main()
