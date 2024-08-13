# main.py
# 主入口

import __init__ as init
import crawler.crawl as cl
import databases.db as db
import download.download_torrents as dt
import ignore.url as url

config = init.config

xml_buffrer_file = config["xml_buffer_file"]
json_buffer_file = config["json_buffer_file"]


# 帮助
def help():
    print("h: help")
    print("q: quit")
    print("r: request")
    print("p: parse")
    print("c: clear")
    print("i: insert")
    print("d: download")
    print("pr: print database")
    return True


# 退出
def quit():
    return False


# 请求
def request():
    inp = input("enter the name of the rss: ")
    if inp in config["url"]:
        cl.crawl(config["url"][inp], xml_buffrer_file)
    else:
        print("rss not found")
    return True


# 解析
def parse():
    inp = input("enter the name of the method: ")
    if inp in url.url_dic:
        parse_method = url.url_dic[inp]["method"]

        with open(xml_buffrer_file, "rb") as f:
            parse_method(f.read(), json_buffer_file)

    else:
        print("method not found")

    return True


# 清除缓存
def clear():
    with open(json_buffer_file, "w") as f:
        f.write("")

    with open(xml_buffrer_file, "w") as f:
        f.write("")

    print("buffer cleared")

    return True


# 插入数据库
def insert():
    db.insert_data(json_buffer_file)
    return True


# 下载
def download():
    data_lists = db.get_torrent_data_that_isnt_downloaded()
    downloaded_id = dt.download_torrent(data_lists)
    db.update_data_is_downloaded(downloaded_id)
    return True


# 打印数据库
def print_database():
    db.export_to_file("./ignore/data.csv")
    return True


# 命令字典
cmd_dic = {
    "h": help,  # 帮助
    "q": quit,  # 退出
    "r": request,  # 请求
    "p": parse,  # 解析
    "c": clear,  # 清除缓存
    "i": insert,  # 插入
    "d": download,  # 下载
    "pr": print_database,  # 打印数据库
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
