"""使用facebook-scraper对Facebook进行爬取，不用使用API"""
from datetime import datetime
from typing import Any

import facebook_scraper
import json
from requests.cookies import RequestsCookieJar
import os
import time


class DateEncoder(json.JSONEncoder):
    """json.dumps默认无法将datetime类型的属性进行序列化，因此需要额外增加解析器"""

    def default(self, o: Any) -> Any:
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, o)


def scrap_without_cookie():
    group_list = ['COVID19Resources',
                  373920943948661, 1288475234841795, 256933822441031, 1047666978949055, 'solidaritycandle',
                  'VancouverIslandEmergencyPreparedness', 1288475234841795, 891546924927251, ]
    my_scraper = facebook_scraper._scraper
    my_scraper.user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/88.0.4324.146 Safari/537.36 Edg/88.0.705.62"
    )
    my_scraper.cookie = ("sb=ZSu7X0nIEY9Mb2gb5-_vzxTe; "
                         "datr=ZSu7X9aILwqfhmrzhEuXDtqd; "
                         "_fbp=fb.1.1610674279287.2026618001; "
                         "locale=en_US; wd=1440x796; "
                         "c_user=100009018647083; "
                         "spin=r.1003264875_b.trunk_t.1612428646_s.1_v.2_; "
                         "presence=EDvF3EtimeF1612489368EuserFA21B09018647083A2EstateFDutF0CEchF_7bCC; "
                         "xs=19%3Anx2rLxT33gUAlw%3A2%3A1612428642%3A16804%3A8668%3A%3AAcV_cf-bvvG3dcYEEU-ewMBnuir8pVW7WOS8aAFHBA; "
                         "fr=1yiV9hm7zUnVWlv1j.AWXXogAarLNdG_u00cJlBCjZ8Dk.Bfuytl.KB.F_9.0.0.BgHQBp.AWWcpIXb_mg")
    for group_id in group_list:
        print(f'Processing Group[{group_id}]')
        for index, post in enumerate(facebook_scraper.get_posts(group=group_id, pages=500)):
            with open(os.path.join('COVID-19-FACEBOOK', f'{post["post_id"]}.json'), 'w') as file_handler:
                print(f"Saving file{index} with post_id={post['post_id']}")
                file_handler.write(json.dumps(post, indent=1, cls=DateEncoder))
        print(f'Done Group[{group_id}]')
        time.sleep(15)


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
