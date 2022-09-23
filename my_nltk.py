import nltk
import re
import json
import os
from wordcloud import WordCloud
# from nltk.book import text1,  FreqDist
from nltk.probability import FreqDist
from nltk.sentiment import SentimentIntensityAnalyzer
from urllib import request
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


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


def test_clean_text():
    stopwords = nltk.corpus.stopwords.words('english') + ["RT", "rt", ":", ",", "'", '•', '-', 'still', "day",
                                                          "later", "1", "first", "take", "get"]
    with open("/Users/leihuang/Work/pycharm-workspace/COVID-DATASET/pos/pos.txt") as file_handler:
        text = file_handler.read()
    text1 = text.split()
    reg1 = r"^@\w+:$"  # @user_name:形式
    reg2 = r"^https://"
    reg3 = r"[,.]$|^#"
    lemmatizer = nltk.stem.WordNetLemmatizer()
    porter = nltk.PorterStemmer()
    # text = [lemmatizer.lemmatize(re.sub(reg3, "", w.lower())) for w in text1 if
    #         w.lower() not in stopwords and not re.match(reg1, w)
    #         and not re.match(reg2, w)]
    text = []
    for word in text1:
        w = word.lower()
        if w.lower() in stopwords or re.match(reg1, w) or re.match(reg2, w):
            continue
        elif w == "covid" or w == "covid19":
            w = "covid-19"
        elif w == "dy" or w == "died":
            w = "die"
        elif w == "death.365":
            w = "death"
        elif w == "#covid19vaccine":
            w = "vaccine"
        elif w == "dr":
            w = 'doctor'
        elif 'xoxo' in w:
            continue

        w = re.sub(reg3, "", w)
        # text.append(lemmatizer.lemmatize(re.sub(reg3, "", w.lower())))
        text.append(porter.stem(w))
    return text


def test_frequency_distribution():
    # text = test_clean_text()
    # text = "RT @BNODesk: 1 year ago today: Dr. Li Wenliang dies of COVID-19, more than a month " \
    #        "after he was accused of spreading rumors about a virus o…"
    with open("/Users/leihuang/Work/pycharm-workspace/COVID-DATASET/pos/pos.txt") as file_handler:
        text = file_handler.read()
    text1 = nltk.Text(nltk.tokenize.word_tokenize(text))
    fdist1 = FreqDist(text1)
    print(fdist1)
    print(fdist1.most_common(100))

    test_concordance(text1, 'vaccine')

    # fdist1.plot(50, cumulative=True)
    # 返回低频项列表
    # print(fdist1.hapaxes())
    # 查找超过15个字母的单词
    # print([w for w in set(text1) if len(w) > 15])

    # fdist5 = FreqDist(text1)
    # print(sorted([w for w in set(text1) if len(w) > 7 and fdist5[w] > 7]))
    # fdist5.tabulate()


def test_word_cloud():
    neg_word_dic = dict([
        # ('covid-19', 40827),
        ('vaccine', 11874), ('die', 9400), ('death', 8298),
        ('us', 5352), ('fight', 4204),
        ('home', 3764), ('say', 3437), ('health', 3277),
        ('case', 3213), ('ago', 3194), ('dead', 3081), ('found', 3005),
        ('former', 2972), ('tv', 2611),
        ('doctor', 2586), ('stop', 2510),
        ('record', 2465), ('covid19vaccine', 2234), ('virus', 2224),
        ('test', 1987), ('report', 1920), ('infect', 1886),
        ('spread', 1879), ('time', 1825), ('coronavirus', 1811), ('travel', 1794),
        ('month', 1709), ('know', 1703), ('refuse', 1665),
        ('see', 1579), ('black', 1571), ('face', 1490), ('risk', 1414),
        ('site', 1403), ('life', 1402), ('state', 1395), ('system', 1389), ('o…', 1375), ('like', 1363),
        ('last', 1356), ('story', 1348), ('crime', 1321), ('much', 1305), ('threaten', 1283),
        ('family', 1283), ('try', 1248), ('early', 1245), ('hospital', 1240), ('expos', 1236),
        ('fire', 1230), ('country', 1207), ('develop', 1205), ('stolen', 1197),
        ('need', 1181), ('go', 1171), ('covid', 1164), ('want', 1157), ('today:', 1152),
        ('sever', 1152), ('make', 1142), ('worker', 1139), ('American', 1107),
        ('result', 1104), ('track', 1089), ('accept', 1088), ('expect', 1082),
        ('affect', 1065)]
    )
    pos_word_dic = dict([('vaccine', 30677), ('help', 7568), ('family', 6335), ('people', 5661), ('pleasure', 5358),
                    ('approve', 5303), ('dose', 5176), ('like', 4971), ('support', 4945), ('health', 4517),
                    ('safe', 3846), ('thank', 3779), ('need', 3754), ('case', 3721), ('social', 3444), ('care', 3149),
                    ('effect', 3121), ('free', 3119), ('good', 3022), ('action', 3020), ('emergency', 3018),
                    ('know', 2913), ('contain', 2853), ('keep', 2844), ('mask', 2818), ('defense', 2813),
                    ('time', 2796), ('coronavirus', 2793), ('socialdistancing', 2716), ('wear', 2657), ('share', 2647),
                    ('provide', 2595), ('follow', 2573), ('home', 2513), ('request', 2513), ('school', 2395),
                    ('great', 2362), ('top', 2328), ('join', 2320), ('media', 2311), ('group', 2297),
                    ('protect', 2287), ('study', 2280), ('medicine', 2280), ('live', 2152), ('happy', 2123),
                    ('relief', 2064)])
    wc = WordCloud(background_color='white')
    wc.generate_from_frequencies(pos_word_dic)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()


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


def test_normalizing_text():
    raw = """DENNIS: Listen, strange women lying in ponds distributing swords
            is no basis for a system of government.  Supreme executive power derives from
            a mandate from the masses, not from some farcical aquatic ceremony."""
    tokens = nltk.word_tokenize(raw)
    # 1. Stemming使用Stemmers提取词干，推荐使用Porter stemmer
    porter = nltk.PorterStemmer()
    lancaster = nltk.LancasterStemmer()
    print([porter.stem(w) for w in tokens])
    print([lancaster.stem(w) for w in tokens])


def test_vader():
    input_dir = "/Users/leihuang/Work/pycharm-workspace/COVID-DATASET/COVID-19-FACEBOOK"
    pos_dir = "/Users/leihuang/Work/pycharm-workspace/COVID-DATASET/pos"
    neg_dir = "/Users/leihuang/Work/pycharm-workspace/COVID-DATASET/neg"
    neu_dir = "/Users/leihuang/Work/pycharm-workspace/COVID-DATASET/neu"
    json_template = """
    {
        "id":"{id_str}",
        "text":"{text}"
    }
    """
    pos_counter = 0
    neg_counter = 0
    neu_counter = 0
    for file_name in os.listdir(input_dir):
        # print(file_name)
        with open(os.path.join(input_dir, file_name)) as file_handler:
            try:
                json_text = json.load(file_handler)
            except UnicodeDecodeError:
                pass
        sia = SentimentIntensityAnalyzer()
        # id_str = json_text["id_str"]
        try:
            text: str = json_text['text'].replace("\n", "")
        except (KeyError, AttributeError):
            # print(id_str)
            pass
        print(text)
        polarity_socre: dict = sia.polarity_scores(text)
        if polarity_socre["compound"] > 0:
            pos_counter += 1
            with open(os.path.join(pos_dir, "pos.txt"), "a") as output_file:
                output_file.write(text)
                output_file.write("\n")
        elif polarity_socre["compound"] < 0:
            neg_counter += 1
            with open(os.path.join(neg_dir, "neg.txt"), "a") as output_file:
                output_file.write(text)
                output_file.write("\n")
        else:
            neu_counter += 1
            with open(os.path.join(neu_dir, "new.txt"), "a") as output_file:
                output_file.write(text)
                output_file.write("\n")
    total = pos_counter + neg_counter + neu_counter
    print(f"""Total records: {total}. 
    Pos records: {pos_counter}({pos_counter * 100 / total}).
    Neg records: {neg_counter}({neg_counter * 100 / total}).
"""
          )


def test_ie_preprocess():
    """测试信息提取的预处理部分，即Sentence Segmentation、Tokenization、PoS Tagging"""
    document2 = """
    Data journalist Annie Gouk has done a number of “deep-dive” investigations into local data surrounding important 
    social issues. 
    You can see some of her previous work around racial inequality here, or different aspects of the gender gap here.
    """
    document = "My mom was admitted to the hospital on 2/12."
    sentences = nltk.sent_tokenize(document)
    tokens = [nltk.word_tokenize(sent) for sent in sentences]
    pos_tags = [nltk.pos_tag(token) for token in tokens]
    print(pos_tags)
    print(nltk.corpus.treebank.tagged_sents()[22])
    # for pos_tag in pos_tags:
    #     print(nltk.ne_chunk(pos_tag, binary=False))
    grammar = r"""NP: {<DT>?<PRP.*>?<JJ.*>*<NN.*>*}
    VP: {<VB.*>*}
    CLAUSE: {(<IN>?<DT>?<JJ.*>*<NN.*>*)?}"""
    cp = nltk.RegexpParser(grammar)
    for pos_tag in pos_tags:
        print(cp.parse(pos_tag))
    tree1 = nltk.Tree('NP', ["My mom"])
    tree2 = nltk.Tree('VP', ["was admitted"])
    tree3 = nltk.Tree('TO', ["to"])
    tree4 = nltk.Tree('NP', ["the hospital"])
    tree5 = nltk.Tree('CLAUSE', ['on 2/12.'])

    my_tree = nltk.Tree("S", [tree1, tree2, tree3, tree4, tree5])
    my_tree.draw()


if __name__ == '__main__':
    # nltk.download()
    # test_concordance(text2, "monstrous")
    # test_concordance(text2, "very")
    # test_similar([text1, text2], "monstrous")
    # test_common_contexts(text2, ['monstrous', 'very'])
    # test_dispersion_plot(text4, ["citizens", "democracy", "freedom", "duties", "America"])
    # test_generate(text1)
    # print(__lexical_diversity(text3))
    test_frequency_distribution()
    # test_collocations()
    # test_ebooks()
    # test_html()
    # test_re()
    # test_normalizing_text()
    # test_vader()
    # test_ie_preprocess()
    # test_word_cloud()
