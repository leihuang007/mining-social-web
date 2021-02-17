import nltk
import re
# from nltk.book import text1,  FreqDist
from nltk.probability import FreqDist
from urllib import request
from bs4 import BeautifulSoup


def __my_separator(function_name: str, name: str):
    print('-' * 50 + function_name + '-' * 50)
    print(name)


def __lexical_diversity(my_text: nltk.text.Text):
    """计算词汇复杂度"""
    return len(set(my_text)) / len(my_text)


def test_concordance(my_text: nltk.text.Text, keyword: str):
    """显示词语索引"""
    __my_separator("test_concordance", my_text.name)
    print(my_text.concordance(keyword))


def test_similar(my_texts: list, keyword: str):
    for text in my_texts:
        __my_separator("test_similar", text.name)
        print(text.similar(keyword))


def test_common_contexts(my_text: nltk.text.Text, keyword_list):
    __my_separator("test_common_contexts", my_text.name)
    print(my_text.common_contexts(keyword_list))


def test_dispersion_plot(my_text: nltk.text.Text, keyword_list: list):
    __my_separator("test_dispersion_plot", my_text.name)
    my_text.dispersion_plot(keyword_list)


def test_generate(my_text: nltk.text.Text):
    __my_separator("test_generate", my_text.name)
    print(my_text.generate())


def test_frequency_distribution():
    text1 = nltk.Text("")
    fdist1 = FreqDist(text1)
    print(fdist1)
    print(fdist1.most_common(50))
    # fdist1.plot(50, cumulative=True)
    # 返回低频项列表
    print(fdist1.hapaxes())
    # 查找超过15个字母的单词
    print([w for w in set(text1) if len(w) > 15])

    fdist5 = FreqDist(text1)
    print(sorted([w for w in set(text1) if len(w) > 7 and fdist5[w] > 7]))
    fdist5.tabulate()


def test_collocations():
    """显示词组"""
    text1 = nltk.Text("")
    print(text1.collocations())


def test_ebooks():
    with request.urlopen('http://www.gutenberg.org/files/2554/2554-0.txt') as response:
        raw = response.read().decode('utf8')
        # print(raw)
    tokens = nltk.word_tokenize(raw[raw.find('PART I'):raw.rfind("End of Project Gutenberg’s Crime and Punishment")])
    my_text = nltk.Text(tokens)
    print(my_text)
    print(my_text.collocations())


def test_html():
    url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
    with request.urlopen(url) as response:
        raw = response.read().decode('utf8')
    bs_raw = BeautifulSoup(raw, 'html.parser').get_text()
    tokens = nltk.word_tokenize(bs_raw)
    text = nltk.Text(tokens)

    print(text.concordance("gene"))


def test_re():
    wordlist = [w for w in nltk.corpus.words.words('en') if w.islower()]
    # print(wordlist)
    # 查找以ed结尾的单词
    print([w for w in wordlist if re.search("ed$", w)])
    # 查找第三个字母是j，第六个字母是t的八位单词
    print([w for w in wordlist if re.search("^..j..t..$", w)])
    # 计算email或者e-mail出现的次数
    print(sum(1 for w in wordlist if re.search('^e-?mail$', w)))
    # 在T9输入法中键入4653可以出现哪些字
    print([w for w in wordlist if re.search('^[ghi][mno][jlk][def]$', w)])
    # 在聊天记录中查找叠字
    chat_words = sorted(set(w for w in nltk.corpus.nps_chat.words()))
    print([w for w in chat_words if re.search('^m+i+n+e+$', w)])
    print([w for w in chat_words if re.search('^[ha]+$', w)])
    # 在聊天记录中查找不包含元音的单词
    print([w for w in wordlist if re.search('^[^aeiouAEIOU]+$', w)])
    # 找到单词中的所有元音，并计数
    word = 'fjoeiwuoijfkldnanvcmnvam,jrfwioeuofiujdiosjafkl;sdjfklhagkdkslajfk;joiwqueoiuroiytgioyhoihgvz;'
    print(re.findall(r"[aeiou]", word))
    print(len(re.findall(r"[aeiou]", word)))


if __name__ == '__main__':
    # nltk.download()
    # test_concordance(text2, "monstrous")
    # test_concordance(text2, "very")
    # test_similar([text1, text2], "monstrous")
    # test_common_contexts(text2, ['monstrous', 'very'])
    # test_dispersion_plot(text4, ["citizens", "democracy", "freedom", "duties", "America"])
    # test_generate(text1)
    # print(__lexical_diversity(text3))
    # test_frequency_distribution()
    # test_collocations()
    # test_ebooks()
    # test_html()
    test_re()
