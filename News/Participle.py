import jieba
import pymysql

# 创建停用词列表
def stopwordslist():
    stopwords = [line.strip() for line in open('stop_words.txt', encoding='UTF-8').readlines()]
    return stopwords
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

# 对句子进行中文分词
def seg_depart(sentence):
    # 对文档中的每一行进行中文分词
    print("正在分词")
    str=''.join(sentence)
    sentence_depart = jieba.cut(str,cut_all=False)
    #print(sentence_depart)
    # 创建一个停用词列表
    stopwords = stopwordslist()
    # 输出结果为outstr
    outstr = ''
    # 去停用词
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr

lists = connect_Mysql()
conn = pymysql.connect(host='127.0.0.1',
                           user='guxiguo',
                           password='520134',
                           port=3306,
                           # db='student',
                           db='NewsRecommend',
                           charset='utf8')
i = 1
for line in lists:
    print(line)
    result = seg_depart(line)
    print(result)
    sql = "select news_title from News where news_id=%s;"
    j = (i)
    cur = conn.cursor()
    cur.execute(sql, j)
    title = cur.fetchall()[0][0]
    insert = "insert into newsparticiple (news_id,news_title,news_participle) values (%s,%s,%s);"
    data = (i, title, result)
    cur.execute(insert, data)
    conn.commit()
    i = i+1
cur.close()
conn.close()