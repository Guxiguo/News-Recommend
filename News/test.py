import xlrd
import jieba
import pymysql

#打开停用词表，返回一个停用词列表
def stopwordslist():
    stopwords = [line.strip() for line in open('D:/NewsRecommend/News/stop_words.txt', encoding='UTF-8').readlines()]
    return stopwords


def connect_Mysql():
    conn = pymysql.connect(host='127.0.0.1',
                           user='guxiguo',
                           password='520134',
                           port=3306,
                           # db='student',
                           db='NewsRecommend',
                           charset='utf8')
    sql = "select news_content from news;"
    cur = conn.cursor()
    cur.execute(sql)
    list = cur.fetchall()
    cur.close()
    conn.close()
    return list

def seg_depart(sentence):
    # 对文档中的每一行进行中文分词
    print("正在分词")
    str=''.join(sentence)
    sentence_depart = jieba.cut(str, cut_all=False)
    #print(sentence_depart)
    # 创建一个停用词列表
    stopwords = stopwordslist()
    # 输出结果为outstr
    outstr = ()
    # 去停用词
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += (word,)
                #outstr += " "
    return outstr

def ReadWord(excle):
    wb = xlrd.open_workbook(excle)
    # 第二步：选取表单
    sh = wb.sheet_by_name('Sheet1')
    row = sh.nrows
    #print(row)
    clo = sh.ncols
    #print(clo)
    dict = {}
    for i in range(1, 27467):
        list = sh.row_values(i, 0, 12)
        word = list[0]
        classify = list[4]
        list.clear()
        dict[word] = classify
    return dict

def Classify(dict, words):
    le = 0
    hao = 0
    nu = 0
    ai = 0
    ju = 0
    e = 0
    jing = 0
    #print(dict.keys())
    #print(words)
    for word in words:
        print(word)
        if word in dict.keys():
            value = dict[word]
            if value == 'PA' or value == 'PE':
                le = le+1
            if value == 'PD' or value == 'PH' or value == 'PG' or value == 'PB' or value == 'PK':
                hao = hao+1
            if value == 'NA':
                nu = nu + 1
            if value == 'NB' or value == 'NJ' or value == 'NH' or value == 'PF':
                ai = ai + 1
            if value == 'NI' or value == 'NG' or value == 'NC':
                ju = ju + 1
            if value == 'NE' or value == 'ND' or value == 'NN' or value == 'NK' or value == 'NL':
                e = e + 1
            if value == 'PC':
                jing = jing + 1
    sum = {'乐': le, '好': hao, '怒': nu, '哀': ai, '俱': ju, '恶': e, '惊': jing}
    return sum

lists = connect_Mysql()
dicc = ReadWord('emotion.xlsx')
for line in lists:
    #print(line)
    result = seg_depart(line)
    d = Classify(dicc, result)
    print(d)
    #print(result)
    '''sql = "select news_title from News where news_id=%s;"
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
conn.close()'''
#print(ReadWord('emotion.xlsx'))