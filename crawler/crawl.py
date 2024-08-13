#

import fake_useragent
import requests

ua = fake_useragent.UserAgent()

save_path = "./crawler/data.xml"


def crawl(url):
    print("getting response...")
    xml = requests.get(url, headers={"User-Agent": ua.random}).content
    print("response received")

    with open(save_path, "wb") as f:
        f.write(xml)

    print("data saved to " + save_path)


def main():
    url = "https://mikanani.me/RSS/MyBangumi?token=xzis5q9HJHqZudKJbY7KL2bci%2bAmLEJ9URet6OgIaoQ%3d"
    crawl(url)


if __name__ == "__main__":
    main()
