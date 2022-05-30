
import xlrd
import jieba
import pymysql

#打开停用词表，返回一个停用词列表
def stopwordslist():
    stopwords = [line.strip() for line in open('D:/NewsRecommend/News/stop_words.txt', encoding='UTF-8').readlines()]
    return stopwords

#连接MySQL数据库并且查询news表中的news_content内容
def connect_Mysql():
    conn = pymysql.connect(host='127.0.0.1',
                           user='guxiguo',
                           password='520134',
                           port=3306,
                           # db='student',
                           db='NewsRecommend',
                           charset='utf8')
    sql = "select news_content from News;"
    cur = conn.cursor()
    cur.execute(sql)
    list = cur.fetchall()
    cur.close()
    conn.close()
    return list

#对新闻内容进行分词
#sentence是新闻内容
def seg_depart(sentence):
    # 对文档中的每一行进行中文分词
    str=''.join(sentence)
    sentence_depart = jieba.cut(str, cut_all=False)
    # 创建一个停用词列表
    stopwords = stopwordslist()
    # 输出结果为outstr
    outstr = ()
    # 去停用词
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += (word,)
    return outstr

#读取情感词典文件中的内容，返回字典
#excel是文件名称
def ReadWord(excle):
    wb = xlrd.open_workbook(excle)
    # 第二步：选取表单
    sh = wb.sheet_by_name('Sheet1')
    row = sh.nrows
    #print(row)
    clo = sh.ncols
    #print(clo)
    dict = {}
    for i in range(1, 114768):
        list = sh.row_values(i, 0, 2)
        word = list[0]
        score = list[1]
        list.clear()
        dict[word] = score
    return dict
#读取否定词
def ReadPrivate(excel):
     wb = xlrd.open_workbook(excel)
     # 第二步：选取表单
     sh = wb.sheet_by_name('Sheet1')
     #row = sh.nrows
     list = sh.col_values(0)
     list.pop(0)
     return list

#读取程度词
def ReadMost(excel):
    wb = xlrd.open_workbook(excel)
    # 第二步：选取表单
    sh = wb.sheet_by_name('Sheet1')
    most_dic = {}
    for i in range(1, sh.nrows):
        list = sh.row_values(i, 0, 2)
        most_dic[list[0]] = list[1]
    return most_dic

#统计正面词语以及负面词语出现的次数
#dict为情感词典
#words为分词结果
def Classify(dict, words):
    pos = 0
    neg = 0
    #print(dict.keys())
    #print(words)
    for word in words:
        #print(word)
        if word in dict.keys():
            value = dict[word]
            if value > 0:
                pos = pos+1
            elif value < 0:
                neg = neg+1
    sum = {'正面': pos,  '负面': neg}
    return sum


def socre_sentiment(sen_word, not_word, degree_word, seg_result):
    # 权重初始化为1
    W = 1
    score = 0
    # 情感词下标初始化
    sentiment_index = -1
    # 情感词的位置下标集合
    sentiment_index_list = list(sen_word.keys())
    # 遍历分词结果(遍历分词结果是为了定位两个情感词之间的程度副词和否定词)
    for i in range(0, len(seg_result)):
        # 如果是情感词（根据下标是否在情感词分类结果中判断）
        if i in sen_word.keys():
            # 权重*情感词得分
            score += W * sen_word[i]
            # 情感词下标加1，获取下一个情感词的位置
            sentiment_index += 1
            if sentiment_index < len(sentiment_index_list) - 1:
                # 判断当前的情感词与下一个情感词之间是否有程度副词或否定词
                for j in (sentiment_index_list[sentiment_index], sentiment_index_list[sentiment_index + 1]):
                    # 更新权重，如果有否定词，取反
                    if j in not_word:
                        W *= -1
                    elif j in degree_word.keys():
                        # 更新权重，如果有程度副词，分值乘以程度副词的程度分值
                        W *= degree_word[j]
        # 定位到下一个情感词
        if sentiment_index < len(sentiment_index_list) - 1:
            i = sentiment_index_list[sentiment_index + 1]
    return score


#计算相似度
#def Similarity():
#插入情感得分到数据库
def Update_Mysql(score, news_id):
    conn = pymysql.connect(host='127.0.0.1',
                           user='guxiguo',
                           password='520134',
                           port=3306,
                           # db='student',
                           db='NewsRecommend',
                           charset='utf8')
    sql = "update newsparticiple set emotion_score='%s' where news_id='%s';"
    data = (score, news_id)
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    cur.close()
    conn.close()


lists = connect_Mysql()
dicc = ReadWord('D:/NewsRecommend/News/BosonNLP_sentiment_score.xls')
most_dic = ReadMost('D:/NewsRecommend/News/most.xlsx')
private = ReadPrivate('D:/NewsRecommend/News/privative.xlsx')
news_id = 1
for line in lists:
    print(line)
    result = seg_depart(line)
    d = Classify(dicc, result)
    s = socre_sentiment(dicc, private, most_dic, result)
    Update_Mysql(s, news_id)
    news_id += 1
    print(d, s)
