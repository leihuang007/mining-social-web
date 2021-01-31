import twitter
import json
from urllib.parse import unquote
from collections import Counter
from prettytable import PrettyTable
import os


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
    """获取热点话题Set之间的共性。"""
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


def search_twitter(q: str = "COVID-19", count: int = 1000, times: int = 1, is_local: bool = True) -> list:
    """根据指定关键词搜索，并返回list
    q -- 需要搜索的关键词
    count -- 每次搜索的数量
    times -- 要搜索的次数
    is_local -- 是否使用本地缓存的搜索结果
    """
    if not is_local:
        my_twitter_api = generate_twitter_api()

        search_results = my_twitter_api.search.tweets(q=q, count=count, lang="en")
        print(f"{search_results.rate_limit_remaining=}")
        statuses = search_results['statuses']

        for _ in range(times):
            # print('Length of statuses', len(statuses))
            try:
                next_results = search_results['search_metadata']['next_results']
            except KeyError:  # No more results when next_results doesn't exist
                break

            kwargs = dict([kv.split('=') for kv in unquote(next_results[1:]).split("&")])

            search_results = my_twitter_api.search.tweets(**kwargs)
            statuses += search_results['statuses']
            print(f"{search_results.rate_limit_remaining=}")
            print(f'Appending {_ + 1} time(s). Found {len(statuses)} statuses')

            # print(json.dumps(statuses[0], indent=1))
        print(f'Done searching. Found {len(statuses)} statuses.')
        return statuses
    elif is_local:
        print(f'Using local search results. Located in "{q}"')
        files = os.listdir(q)
        statuses = []
        if files:
            print(f'Found {len(files)} files.')
            for file in files:
                with open(os.path.join(q, file)) as result_file:
                    statuses.append(json.loads(result_file.read()))
            return statuses


def save_statuses_to_file(statuses: list, dir_name: str):
    """将statuses保存到dir_name指定的文件夹下，文件名为每个status的id"""
    for index, status in enumerate(statuses):
        with open(f"{dir_name}\\{status['id']}.json", 'w') as file:
            file.write(json.dumps(status, indent=1))


def save_statuses_to_one_file(statuses: list):
    with open("COVID-19\\statuses_all.txt", "w") as file_handler:
        file_handler.write(json.dumps(statuses, indent=1))


def extract_text_screen_names_hash_tags():
    statuses = search_twitter()
    save_statuses_to_one_file(statuses)
    status_texts = [status['text'] for status in statuses]
    screen_names = [user_mention['screen_name'] for status in statuses for user_mention in
                    status['entities']['user_mentions']]
    hashtags = [hashtag['text'] for status in statuses for hashtag in status['entities']['hashtags']]
    words = [word for sentence in status_texts for word in sentence.split()]
    # print(status_texts)
    # print(screen_names)
    # print(hashtags)
    # print(words)

    for item in [words, screen_names, hashtags]:
        c = Counter(item)
        print(c.most_common()[:10])
    return words, screen_names, hashtags


def pretty_extract_text():
    """使用prettytable对字频结果进行美化"""
    words, screen_names, hashtags = extract_text_screen_names_hash_tags()
    for label, data in (("Words", words), ("Screen Names", screen_names), ("Hashtags", hashtags)):
        pt = PrettyTable(field_names=[label, "Count"])
        c = Counter(data)
        [pt.add_row(kv) for kv in c.most_common()[0:10]]
        pt.align[label], pt.align["Count"] = 'l', 'r'
        print(pt)


def lexical_diversity(tokens: list):
    """计算Lexical Diversity"""
    return len(set(tokens)) / len(tokens)


def average_words_per_tweet(statuses):
    word_counts = sum([word for status in statuses for word in status.split()])
    return word_counts / len(statuses)


def find_most_retweeted():
    """按照被retweet的次数进行排序"""
    statuses = search_twitter()
    retweet = [(status['retweet_count'], status['retweeted_status']['user']['screen_name'], status['text'])
               for status in statuses if "retweeted_status" in status.keys()]
    pt = PrettyTable(field_names=['Count', 'Screen Name', 'Text'])
    [pt.add_row(row) for row in sorted(retweet, reverse=True)]
    pt.max_width['Text'] = 50
    pt.align = 'l'
    print(pt)


if __name__ == '__main__':
    find_most_retweeted()
    # statuses = search_twitter(count=100, times=3)
    # save_statuses_to_file(statuses, dir_name='COVID-19')
