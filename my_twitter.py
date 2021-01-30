import twitter
import json
from urllib.parse import unquote


def generate_twitter_api() -> twitter.Twitter:
    """获取twitter链接"""
    with open('twitter_api.json') as tf_conf:
        _twitter_config_json = json.load(tf_conf)
        consumer_key = _twitter_config_json['consumer_key']
        consumer_secret = _twitter_config_json['consumer_secret']
        bearer_token = _twitter_config_json['bearer_token']

    auth = twitter.oauth2.OAuth2(consumer_key, consumer_secret, bearer_token)
    twitter_api = twitter.Twitter(auth=auth)

    # print(twitter_api)
    return twitter_api


def get_trends(twitter_api: twitter.Twitter, wod_id: int):
    """根据国家编码获取该国家的热点话题"""
    trends = twitter_api.trends.place(_id=wod_id)
    return trends


def beautiful_trends_to_str(trends) -> str:
    """将热点话题美化为标准的JSON格式"""
    __trends = json.dumps(trends, indent=1)
    return __trends


def trends_to_set(trends):
    """将热点话题转化为Set"""
    __trend_set = set([trend['name'] for trend in trends[0]['trends']])
    return __trend_set


def trends_to_list(trends) -> list:
    """将热点话题name提取出后排名"""
    _trend_list = [trend['name'] for trend in trends[0]['trends']]
    return _trend_list


def compare_trends():
    """获取热点话题Set之间的共性。common trends: {'YG Plus', '#NCT127DAY', 'bighit'}"""
    # The Yahoo! Where On Earth ID for the entire world is 1.
    world_woe_id = 1
    us_woe_id = 23424977

    my_twitter_api = generate_twitter_api()

    world_trends = get_trends(my_twitter_api, world_woe_id)
    world_trends_set = trends_to_set(world_trends)
    print('world trends: ' + str(world_trends_set))

    us_trends = get_trends(my_twitter_api, us_woe_id)
    us_trends_set = trends_to_set(us_trends)
    print('us trends: ' + str(us_trends_set))

    common_trends = world_trends_set.intersection(us_trends_set)
    print('common trends: ' + str(common_trends))


def list_trend():
    """获取指定国家的Trending"""
    us_woe_id = 23424977
    my_twitter_api = generate_twitter_api()
    us_trends = get_trends(my_twitter_api, us_woe_id)
    us_trend_list = trends_to_list(us_trends)
    print(us_trend_list)


def search_twitter():
    q = "YG Plus"
    count = 100

    my_twitter_api = generate_twitter_api()

    search_results = my_twitter_api.search.tweets(q=q, count=count)
    statuses = search_results['statuses']

    for _ in range(5):
        print('Length of statuses', len(statuses))
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError:  # No more results when next_results doesn't exist
            break

        kwargs = dict([kv.split('=') for kv in unquote(next_results[1:]).split("&")])

        search_results = my_twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']

        print(json.dumps(statuses[0], indent=1))


if __name__ == '__main__':
    list_trend()