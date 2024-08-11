# 解析 XML 数据

from lxml import etree


# 解析 XML 数据，返回字典列表
def get_data(xml):
    # 解析 XML 数据
    root = etree.fromstring(xml)

    data_list = []  # 遍历每个 <item> 元素，并存到data
    torrent_data = []
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
        torrent_data.append(
            {
                "torrent_name": dic["title"],
                "torrent_pub_date": dic["pub_date"],
                "torrent_link": dic["enclosure_url"],
            }
        )

    # 返回数据
    return {"data_list": data_list, "torrent_data": torrent_data}
