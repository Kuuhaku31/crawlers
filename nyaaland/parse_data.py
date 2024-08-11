# 解析 XML 数据

from lxml import etree

"""
<item>
    <title>拳奴死闘伝セスタス 第01-11巻 [Kendo Shitouden Cestvs vol 01-11]</title>
    <link>https://nyaa.land/download/1858417.torrent</link>
    <guid isPermaLink="true">https://nyaa.land/view/1858417</guid>
    <pubDate>Sun, 11 Aug 2024 13:31:38 -0000</pubDate>
    <nyaa:seeders>1</nyaa:seeders>
    <nyaa:leechers>3</nyaa:leechers>
    <nyaa:downloads>0</nyaa:downloads>
    <nyaa:infoHash>d2d3cbee40b26629af5529c1818cb21d18e514d3</nyaa:infoHash>
    <nyaa:categoryId>3_3</nyaa:categoryId>
    <nyaa:category>Literature - Raw</nyaa:category>
    <nyaa:size>1.2 GiB</nyaa:size>
    <nyaa:comments>0</nyaa:comments>
    <nyaa:trusted>No</nyaa:trusted>
    <nyaa:remake>No</nyaa:remake>
    <description>
        <![CDATA[ <a href="https://nyaa.land/view/1858417">#1858417 | 拳奴死闘伝セスタス 第01-11巻 [Kendo Shitouden Cestvs vol 01-11]</a> | 1.2 GiB | Literature - Raw | D2D3CBEE40B26629AF5529C1818CB21D18E514D3 ]]>
    </description>
</item>
"""


# 针对 nyaa.land 的 RSS 数据解析
# 解析 XML 数据，返回字典列表
def get_data(xml):
    # 解析 XML 数据
    root = etree.fromstring(xml)

    data_list = []  # 遍历每个 <item> 元素，并存到data
    torrent_data = []

    # 定义命名空间映射
    namespaces = {
        "nyaa": "https://nyaa.land/xmlns/nyaa",
        "atom": "http://www.w3.org/2005/Atom",
    }
    for item in root.xpath("//item"):

        # 用字典存储信息
        dic = {}

        # 提取基本信息
        dic["title"] = item.find("title").text if item.find("title") is not None else ""
        dic["link"] = item.find("link").text if item.find("link") is not None else ""
        dic["guid"] = item.find("guid").text if item.find("guid") is not None else ""
        dic["guid_isPermaLink"] = (
            item.find("guid").get("isPermaLink")
            if item.find("guid") is not None
            else "None"
        )
        dic["pubDate"] = (
            item.find("pubDate").text if item.find("pubDate") is not None else ""
        )
        dic["nyaa:seeders"] = (
            item.find("nyaa:seeders", namespaces).text
            if item.find("nyaa:seeders", namespaces) is not None
            else "None"
        )
        dic["nyaa:leechers"] = (
            item.find("nyaa:leechers", namespaces).text
            if item.find("nyaa:leechers", namespaces) is not None
            else "None"
        )
        dic["nyaa:downloads"] = (
            item.find("nyaa:downloads", namespaces).text
            if item.find("nyaa:downloads", namespaces) is not None
            else "None"
        )
        dic["nyaa:infoHash"] = (
            item.find("nyaa:infoHash", namespaces).text
            if item.find("nyaa:infoHash", namespaces) is not None
            else "None"
        )
        dic["nyaa:categoryId"] = (
            item.find("nyaa:categoryId", namespaces).text
            if item.find("nyaa:categoryId", namespaces) is not None
            else "None"
        )
        dic["nyaa:category"] = (
            item.find("nyaa:category", namespaces).text
            if item.find("nyaa:category", namespaces) is not None
            else "None"
        )
        dic["nyaa:size"] = (
            item.find("nyaa:size", namespaces).text
            if item.find("nyaa:size", namespaces) is not None
            else "None"
        )
        dic["nyaa:comments"] = (
            item.find("nyaa:comments", namespaces).text
            if item.find("nyaa:comments", namespaces) is not None
            else "None"
        )
        dic["nyaa:trusted"] = (
            item.find("nyaa:trusted", namespaces).text
            if item.find("nyaa:trusted", namespaces) is not None
            else "None"
        )
        dic["nyaa:remake"] = (
            item.find("nyaa:remake", namespaces).text
            if item.find("nyaa:remake", namespaces) is not None
            else "None"
        )
        dic["description"] = (
            item.find("description").text
            if item.find("description") is not None
            else "None"
        )

        # 存储到data_list
        data_list.append(dic)
        torrent_data.append(
            {
                "torrent_name": dic["title"],
                "torrent_pub_date": dic["pubDate"],
                "torrent_link": dic["link"],
            }
        )

    # 返回数据
    return {"data_list": data_list, "torrent_data": torrent_data}
