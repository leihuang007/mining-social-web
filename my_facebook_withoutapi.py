"""使用facebook-scraper对Facebook进行爬取，不用使用API"""
from datetime import datetime
from typing import Any

import facebook_scraper
import json
from requests.cookies import RequestsCookieJar
import os

class DateEncoder(json.JSONEncoder):
    """json.dumps默认无法将datetime类型的属性进行序列化，因此需要额外增加解析器"""

    def default(self, o: Any) -> Any:
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, o)


def scrap_without_cookie():
    group_list = [891546924927251, ]

    for index in range(100):
        with open(os.path.join('haha', f"{index}.json"), 'w') as file_handler:
            print(f"Saving file {index} with post_id={index}")
            file_handler.write(json.dumps('{"haha":"lala"}', indent=1, cls=DateEncoder))
    # for index, post in enumerate(facebook_scraper.get_posts(group=1288475234841795, pages=1)):
    #     with open(f'COVID-19-FACEBOOK\\{post["post_id"]}.json', 'w') as file_handler:
    #         print(f"Saving file{index} with post_id={post['post_id']}")
    #         file_handler.write(json.dumps(post, indent=1, cls=DateEncoder))


def scrap_with_cookie():
    with open('facebook_api.json') as fb_config_file:
        _fb_config = json.load(fb_config_file)
        _str_cookie = _fb_config['cookies']

    my_cookie = RequestsCookieJar()
    [my_cookie.set(cookie.strip().split("=")[0], cookie.strip().split("=")[1]) for cookie in _str_cookie.split(";")]

    my_session = facebook_scraper._scraper.session
    my_session.cookies.update(my_cookie)

    for post in facebook_scraper.get_posts(group=932979303783032, pages=1):
        print(post)


if __name__ == '__main__':
    scrap_without_cookie()
