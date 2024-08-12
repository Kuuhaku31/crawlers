# data_list

import json

import lxml.etree as et

# 日志存储
path = "F:/log.json"
path_xml = "F:/log.xml"


# data_list 是一个列表，其中包含了所有的数据字典
# 可以将这个列表传递给 save_log 函数
# 然后将其保存到一个 JSON 文件中
def save_log(data_list):
    print("saving log to " + path)

    total = 0
    saved = 0
    # 读取现有的 JSON 文件
    with open(path, encoding="utf-8") as file:
        json_data = json.load(file)

        for dic in data_list:
            total += 1
            # 如果没有被添加过
            if dic not in json_data["items"]:
                saved += 1
                # 将新的 item 节点添加到 JSON 数据的顶部
                json_data["items"].insert(0, dic)

    # 保存修改后的 JSON 文件
    with open(path, "w", encoding="utf-8") as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)

    print("log saved, " + str(total) + " items found, " + str(saved) + " items saved")


# 储存xml数据
def save_log_xml(xml):
    print("saving log to " + path)

    data_list = []

    root = et.fromstring(xml)
    for item in root.xpath("//item"):
        data_list.append(item)

    total = 0
    saved = 0
    # 读取现有的 xml 文件
    with open(path_xml, encoding="utf-8") as file:
        # 如果文件为空
        if file.read() == "":
            root = et.Element("root")
            tree = et.ElementTree(root)
            tree.write(path_xml, pretty_print=True, xml_declaration=True, encoding="utf-8")
            xml_data = et.parse(path_xml)
            root = xml_data.getroot()
        else:
            xml_data = et.parse(path_xml)
            root = xml_data.getroot()

        for dic in reversed(data_list):
            total += 1
            # 如果没有被添加过
            if dic not in root:
                saved += 1
                # 将新的 item 节点添加到 xml 数据的顶部
                root.insert(0, dic)

    # 保存修改后的 xml 文件
    with open(path_xml, "wb") as file:
        xml_data.write(file, pretty_print=True, xml_declaration=True, encoding="utf-8")


def read_log():
    ns = {"ns": "https://mikanani.me/0.1/"}  # 定义命名空间映射
    with open(path_xml, encoding="utf-8") as file:
        xml_data = et.parse(file)
        root = xml_data.getroot()

        for item in reversed(root):
            title = item.find("title").text
            link = item.find("link").text
            # 提取 <torrent> 内的信息，需要处理命名空间
            torrent_element = item.find("ns:torrent", ns)
            pub_date = torrent_element.find("ns:pubDate", ns).text
            print("title: " + title + "\nlink: " + link + "\npub_date: " + pub_date + "\n" + "-" * 80)


if __name__ == "__main__":
    read_log()
    # save_log_xml
