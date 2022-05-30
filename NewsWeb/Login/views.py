import datetime
import hashlib
from django.http import HttpResponse
from django.shortcuts import render, redirect
import pymysql
import re
from . import models
# Create your views here.

tag = 0
recommend_flag = True
dic = ()
total_score = 0

def login(request):
    global USER
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password')
        h = hashlib.md5()
        h.update(password1.encode())
        mima = h.hexdigest()
        #print(username, password1)
        a = models.User.objects.filter(username=username, password=mima)
        if a:
            USER = username
            return redirect('recommend.html')
        else:
            msg = '用户不存在'
            #print(msg)
            return render(request, 'login.html', {'msg': msg})
    else:
        #print('111')
        return render(request, 'login.html')
    return render(request, 'login.html')

def register(request):
    result_passws = re.compile(r'^(?=.*\d)(?=.*[a-zA-Z]).{6,20}$')  # 必须包含大写或小写字母和数字的组合，可以使用特殊字符，长度在6-20之间
    if request.method == 'POST':
        username = request.POST.get('username1')
        #print(username)
        sex = request.POST.get('sex')
       # print(sex)
        password = request.POST.get('password1')
        password1 = request.POST.get('password2')
        if not result_passws.match(password) or not result_passws.match(password1):
            msg = '密码必须包含字母和数字！'
            return render(request, 'register.html', {'msg': msg})
        #print(password)
        telephone = request.POST.get('tel')
        phone = re.compile(r"^1[35678]\d{9}$")
        h = hashlib.md5()
        h.update(password.encode())
        mima = h.hexdigest()
        tel = models.User.objects.filter(telephone=telephone)
        if not phone.match(telephone):
            msg = '电话号码格式不正确！'
            return render(request, 'register.html', {'msg': msg})
        elif tel:
            msg = '电话号码已存在！'
            return render(request, 'register.html', {'msg': msg})
        #print(telephone)
        #print('111',username,sex,password,telephone)
        user = models.User.objects.filter(username=username)
        if user:
            msg = '用户已存在'
            #print(msg)
            return render(request, 'register.html', {'msg': msg})
        else:
            #print('222',username, sex, password, telephone)
            models.User.objects.create(username=username, sex=sex, password=mima, telephone=telephone)
            return redirect('login.html')
    else:
        #print('333')
        return render(request, 'register.html')
    return render(request, 'register.html')


def recommend(request):
    global key1
    a = USER
    global tag
    tag = 1
    global dic
    global recommend_flag
    #print(username)

    conn = pymysql.connect(host='127.0.0.1',
                           user='guxiguo',
                           password='520134',
                           port=3306,
                           # db='student',
                           db='NewsRecommend',
                           charset='utf8')
    cur = conn.cursor()
    if recommend_flag:
        recommend_flag = False
        sql = 'select emotion_score from scan where user = %s order by id desc ;'
        #查询浏览记录中的5条数据的情感得分然后计算平均得分
        cur.execute(sql, a)
        dic = cur.fetchall()
        scan_score = 0
        #print('dic', len(dic), len(dic[0]), dic, dic[0],dic[0][0])
        if len(dic) < 5 and len(dic) > 0:
            for count in range(0, len(dic)):
                scan_score = scan_score+float(dic[count][0])
            avg_scan_score = scan_score / len(dic)
        elif len(dic) == 0:
            avg_scan_score = 0
        else:
            for count1 in range(0, 5):
                scan_score = scan_score+float(dic[count1][0])
            avg_scan_score = scan_score / 5
           #5条浏览记录中的平均得分
        #print(scan_score,avg_scan_score)
        sql_collect = 'select emotion_score from collect where user = %s order by id desc ;'
        # 查询收藏记录中的5条数据的情感得分然后计算平均得分
        cur.execute(sql_collect, a)
        dic_collect = cur.fetchall()
        collect_score = 0
        if len(dic_collect) < 5 and len(dic_collect) > 0:
            for count2 in range(0, len(dic_collect)):
                collect_score = collect_score+float(dic_collect[count2][0])
            avg_collect_score = collect_score / len(dic_collect)
        elif len(dic_collect) == 0:
            avg_collect_score = 0
        else:
            for count3 in range(0, 5):
               collect_score = collect_score + float(dic_collect[count3][0])
            avg_collect_score = collect_score / 5
        global total_score
        total_score = Score(avg_scan_score, avg_collect_score)
    #print('collect_dic',len(dic_collect), collect_score, collect_score, avg_collect_score, total_score)
    dicc = {}
    i = 0
    #获取搜索文本框的内容
    key = request.POST.get('search1')
    if dic:
        sql2 = 'select s.news_title,news_link from newsparticiple as s left join news as n on s.news_title=n.news_title where s.emotion_score>=%s and s.emotion_score<=%s order by heat desc;'
        data1 = (total_score - 10, total_score + 10)
        cur.execute(sql2, data1)
        dic3 = cur.fetchall()
        if key != None:
            key1 = key
            return redirect('search.html')
        else:
            for d in dic3:
                i = i + 1
                title = 'title' + str(i)
                link = 'link' + str(i)
                flag = 'flag' + str(i)
                dicc[title] = d[0]
                dicc[link] = d[1]
                t = d[0]
                collect1 = models.Collect.objects.filter(user=a, news_title=t)
                if collect1:
                    dicc[flag] = True
                else:
                    dicc[flag] = False
                if i == 15:
                    break
    else:
        sql3 = 'select s.news_title,news_link from newsparticiple as s left join news as n on s.news_title=n.news_title where heat>=0 order by heat desc ;'
        cur.execute(sql3)
        dic2 = cur.fetchall()
        for d in dic2:
            i = i + 1
            title = 'title' + str(i)
            link = 'link' + str(i)
            flag = 'flag' + str(i)
            dicc[title] = d[0]
            dicc[link] = d[1]
            t = d[0]
            collect1 = models.Collect.objects.filter(user=a, news_title=t)
            if collect1:
                dicc[flag] = True
            else:
                dicc[flag] = False
            if i == 15:
                break
    #热门新闻推荐
    sql4 = 'select s.news_title,news_link from newsparticiple as s left join news as n on s.news_title=n.news_title where heat>=0 order by heat desc ;'
    cur.execute(sql4)
    dic4 = cur.fetchall()
    cur.close()
    conn.close()
    j = 0
    for d in dic4:
        j = j + 1
        title = 'heat_title'+str(j)
        link = 'heat_link'+str(j)
        flag = 'heat_flag' + str(j)
        #print(d,title,link)
        dicc[title] = d[0]
        dicc[link] = d[1]
        t = d[0]
        collect1 = models.Collect.objects.filter(user=a, news_title=t)
        if collect1:
            dicc[flag] = True
        else:
            dicc[flag] = False
        if j == 11:
            break
    dicc['a'] = USER
    return render(request, 'recommend.html', dicc)


def yangshi(request):
    a = USER
    global tag
    global recommend_flag
    recommend_flag = True
    tag = 2
    conn = pymysql.connect(host='127.0.0.1',
                           user='guxiguo',
                           password='520134',
                           port=3306,
                           # db='student',
                           db='NewsRecommend',
                           charset='utf8')
    cur = conn.cursor()
    sql = 'select news_title,news_link, news_source from news where news_source like %s"%%";'
    data = ('央视')
    cur.execute(sql, data)
    dic = cur.fetchall()
    sql3 = 'select s.news_title,news_link from newsparticiple as s left join news as n on s.news_title=n.news_title where heat>=0 order by heat desc ;'
    cur.execute(sql3)
    dic3 = cur.fetchall()
    #print(dic3)

    dicc = {}
    i = 0
    cur.close()
    conn.close()
    for d in dic:
        i = i + 1
        title = 'title' + str(i)
        link = 'link' + str(i)
        flag = 'flag' + str(i)
        # print(d,title,link)
        dicc[title] = d[0]
        dicc[link] = d[1]
        t = d[0]
        collect1 = models.Collect.objects.filter(user=a, news_title=t)
        if collect1:
            dicc[flag] = True
        else:
            dicc[flag] = False
        if i == 15:
            break
    j = 0
    print(dic3)
    for d in dic3:
        j = j + 1
        title = 'heat_title' + str(j)
        link = 'heat_link' + str(j)
        flag = 'heat_flag' + str(j)
        # print(d,title,link)

        dicc[title] = d[0]
        dicc[link] = d[1]
        t = d[0]
        collect1 = models.Collect.objects.filter(user=a, news_title=t)
        if collect1:
            dicc[flag] = True
        else:
            dicc[flag] = False
        if j == 11:
            break
    dicc['a'] = a
    #print(dic)
    return render(request, 'yangshi.html', dicc)

def renming(request):
    a = USER
    global tag
    global recommend_flag
    recommend_flag = True
    tag = 3
    conn = pymysql.connect(host='127.0.0.1',
                           user='guxiguo',
                           password='520134',
                           port=3306,
                           # db='student',
                           db='NewsRecommend',
                           charset='utf8')
    cur = conn.cursor()
    sql = 'select news_title,news_link, news_source from news where news_source like %s"%%";'
    data = ('人民')
    cur.execute(sql, data)
    dic = cur.fetchall()
    sql3 = 'select s.news_title,news_link from newsparticiple as s left join news as n on ' \
           's.news_title=n.news_title where heat>=0 order by heat desc ;'
    cur.execute(sql3)
    dic3 = cur.fetchall()
    cur.close()
    conn.close()
    dicc = {}
    i = 0
    for d in dic:
        i = i + 1
        title = 'title' + str(i)
        link = 'link' + str(i)
        flag = 'flag' + str(i)
        # print(d,title,link)
        dicc[title] = d[0]
        dicc[link] = d[1]
        t = d[0]
        collect1 = models.Collect.objects.filter(user=a, news_title=t)
        if collect1:
            dicc[flag] = True
        else:
            dicc[flag] = False
        if i == 15:
            break
    j = 0
    for d in dic3:
        j = j + 1
        title = 'heat_title' + str(j)
        link = 'heat_link' + str(j)
        flag = 'heat_flag' + str(j)

        dicc[title] = d[0]
        dicc[link] = d[1]
        t = d[0]
        collect1 = models.Collect.objects.filter(user=a, news_title=t)
        if collect1:
            dicc[flag] = True
        else:
            dicc[flag] = False
        if j == 11:
            break
    dicc['a'] = USER
    #print(dic)
    return render(request, 'renming.html', dicc)

def xinghua(request):
    a = USER
    global tag
    global recommend_flag
    recommend_flag = True
    tag = 4
    conn = pymysql.connect(host='127.0.0.1',
                           user='guxiguo',
                           password='520134',
                           port=3306,
                           # db='student',
                           db='NewsRecommend',
                           charset='utf8')
    cur = conn.cursor()
    sql = 'select news_title,news_link, news_source from news where news_source like %s"%%";'
    data = ('新华')
    cur.execute(sql, data)
    dic = cur.fetchall()
    sql3 = 'select s.news_title,news_link from newsparticiple as s left join news as n on s.news_title=n.news_title where heat>=0 order by heat desc ;'
    cur.execute(sql3)
    dic3 = cur.fetchall()
    #print(dic3)
    cur.close()
    conn.close()
    i = 0
    dicc = {}
    for d in dic:
        i = i + 1
        title = 'title' + str(i)
        link = 'link' + str(i)
        flag = 'flag' + str(i)
        # print(d,title,link)
        dicc[title] = d[0]
        dicc[link] = d[1]
        t = d[0]
        collect1 = models.Collect.objects.filter(user=a, news_title=t)
        if collect1:
            dicc[flag] = True
        else:
            dicc[flag] = False
        if i == 15:
            break
    j = 0
    for d in dic3:
        j = j + 1
        title = 'heat_title' + str(j)
        link = 'heat_link' + str(j)
        flag = 'heat_flag' + str(j)
        # print(d,title,link)
        dicc[title] = d[0]
        dicc[link] = d[1]
        t = d[0]
        collect1 = models.Collect.objects.filter(user=a, news_title=t)
        if collect1:
            dicc[flag] = True
        else:
            dicc[flag] = False
        if j == 11:
            break
    dicc['a'] = USER
    #print(dic)
    return render(request, 'xinghua.html', dicc)

def qingnian(request):
    a = USER
    global tag
    global recommend_flag
    recommend_flag = True
    tag = 5
    conn = pymysql.connect(host='127.0.0.1',
                           user='guxiguo',
                           password='520134',
                           port=3306,
                           # db='student',
                           db='NewsRecommend',
                           charset='utf8')
    cur = conn.cursor()
    sql = 'select news_title,news_link, news_source from news where news_source like %s"%%";'
    data = ('中国青年')
    cur.execute(sql, data)
    dic = cur.fetchall()

    sql3 = 'select s.news_title,news_link from newsparticiple as s left join news as n on s.news_title=n.news_title where heat>=0 order by heat desc ;'
    cur.execute(sql3)
    dic3 = cur.fetchall()
    #print(dic3)
    cur.close()
    conn.close()

    i = 0
    dicc = {}
    for d in dic:
        i = i + 1
        title = 'title' + str(i)
        link = 'link' + str(i)
        flag = 'flag' + str(i)
        # print(d,title,link)
        dicc[title] = d[0]
        dicc[link] = d[1]
        t = d[0]
        collect1 = models.Collect.objects.filter(user=a, news_title=t)
        if collect1:
            dicc[flag] = True
        else:
            dicc[flag] = False
        if i == 15:
            break
    j = 0
    for d in dic3:
        j = j + 1
        title = 'heat_title' + str(j)
        link = 'heat_link' + str(j)
        flag = 'heat_flag' + str(j)
        # print(d,title,link)

        dicc[title] = d[0]
        dicc[link] = d[1]
        t = d[0]
        collect1 = models.Collect.objects.filter(user=a, news_title=t)
        if collect1:
            dicc[flag] = True
        else:
            dicc[flag] = False
        if j == 11:
            break
    dicc['a'] = USER
    #print(dic)
    return render(request, 'qingnian.html', dicc)

def zhongguo(request):
    a = USER
    global tag
    global recommend_flag
    recommend_flag = True
    tag = 6
    conn = pymysql.connect(host='127.0.0.1',
                           user='guxiguo',
                           password='520134',
                           port=3306,
                           # db='student',
                           db='NewsRecommend',
                           charset='utf8')
    cur = conn.cursor()
    sql = 'select news_title,news_link, news_source from news where news_source like %s"%%";'
    data = ('中国日报')
    cur.execute(sql, data)
    dic = cur.fetchall()
    sql3 = 'select s.news_title,news_link from newsparticiple as s left join news as n on s.news_title=n.news_title where heat>=0 order by heat desc ;'
    cur.execute(sql3)
    dic3 = cur.fetchall()
    #print(dic3)
    cur.close()
    conn.close()
    i = 0
    dicc = {}
    for d in dic:
        i = i + 1
        title = 'title' + str(i)
        link = 'link' + str(i)
        flag = 'flag' + str(i)
        # print(d,title,link)

        dicc[title] = d[0]
        dicc[link] = d[1]
        t = d[0]
        collect1 = models.Collect.objects.filter(user=a, news_title=t)
        if collect1:
            dicc[flag] = True
        else:
            dicc[flag] = False
        if i == 15:
            break
    j = 0
    for d in dic3:
        j = j + 1
        title = 'heat_title' + str(j)
        link = 'heat_link' + str(j)
        flag = 'heat_flag' + str(j)
        # print(d,title,link)

        dicc[title] = d[0]
        dicc[link] = d[1]
        t = d[0]
        collect1 = models.Collect.objects.filter(user=a, news_title=t)
        if collect1:
            dicc[flag] = True
        else:
            dicc[flag] = False
        if j == 11:
            break
    dicc['a'] = USER
    #print(dic)
    return render(request, 'zhongguo.html', dicc)

def heat(scan, comment, date):
    a = datetime.date.today()
    #a = str(a)
    #c = datetime.datetime.strptime(a, '%Y-%m-%d')
    day = (a - date).days
    #print(day)
    #b = datetime.datetime.strptime(date, '%Y-%m-%d')
    return scan*0.4+comment*0.5-day*0.1

def detail(request):
    a = USER
    link = request.GET.get('link')
    title = request.GET.get('title')
    model = models.Newsparticiple.objects.get(news_title=title)
    c = models.Scan.objects.filter(user=a, news_title=title)
    if c:
        models.Scan.objects.filter(user=a, news_title=title).delete()
        models.Scan.objects.create(user=a, news_title=title, emotion_score=model.emotion_score)
    else:
        models.Scan.objects.create(user=a, news_title=title, emotion_score=model.emotion_score)
    scan = models.News.objects.get(news_title=title)
    s = scan.news_scan+1
    scan.news_scan = s
    heat1 = heat(s, scan.news_comment, scan.news_date)
    model.heat = heat1
    scan.save()
    model.save()

    #print('111',link, title)
    return redirect(link)


def search(request):
    key = request.POST.get('search1')
    print(key)
    a = USER
    global tag
    global recommend_flag
    recommend_flag = True
    tag = 7
    conn = pymysql.connect(host='127.0.0.1',
                           user='guxiguo',
                           password='520134',
                           port=3306,
                           # db='student',
                           db='NewsRecommend',
                           charset='utf8')
    cur = conn.cursor()
    sql = 'select news_title,news_link, news_source from news where news_title like %s"%%";'
    cur.execute(sql, '%'+key1)
    dic = cur.fetchall()
    sql3 = 'select s.news_title,news_link from newsparticiple as s left join news as n on s.news_title=n.news_title where heat>=0 order by heat desc ;'
    cur.execute(sql3)
    dic3 = cur.fetchall()
    # print(dic3)
    cur.close()
    conn.close()
    i = 0
    dicc = {}
    for d in dic:
        i = i + 1
        title = 'title' + str(i)
        link = 'link' + str(i)
        flag = 'flag' + str(i)
        # print(d,title,link)
        dicc[title] = d[0]
        dicc[link] = d[1]
        t = d[0]
        collect1 = models.Collect.objects.filter(user=a, news_title=t)
        if collect1:
            dicc[flag] = True
        else:
            dicc[flag] = False
        if i == 15:
            break
    j = 0
    for d in dic3:
        j = j + 1
        title = 'heat_title' + str(j)
        link = 'heat_link' + str(j)
        flag = 'heat_flag' + str(j)
        # print(d,title,link)

        dicc[title] = d[0]
        dicc[link] = d[1]
        t = d[0]
        collect1 = models.Collect.objects.filter(user=a, news_title=t)
        if collect1:
            dicc[flag] = True
        else:
            dicc[flag] = False
        if j == 11:
            break
    dicc['a'] = USER
    # print(dic)
    return render(request, 'search.html', dicc)
def UserCollect(request):
    a = USER
    global tag
    tag = 8
    conn = pymysql.connect(host='127.0.0.1',
                           user='guxiguo',
                           password='520134',
                           port=3306,
                           # db='student',
                           db='NewsRecommend',
                           charset='utf8')
    cur = conn.cursor()
    sql3 = 'select s.news_title,news_link from collect as s left join news as n on s.news_title=n.news_title where user = %s;'
    cur.execute(sql3, a)
    dic3 = cur.fetchall()
    dicc = {}
    title_list = []
    link_list = []
    flag_list = []
    star_list = []
    i = 0
    for new in dic3:
        i = i+1
        star = 'star'+str(i)
        title_list.append(new[0])
        link_list.append(new[1])
        flag_list.append(True)
        star_list.append(star)

    foo = zip(title_list, link_list, flag_list,star_list)
    dicc['foo'] = foo
    dicc['a'] = USER
    return render(request, 'usercollect.html', dicc)


def collect(request):
    a = USER
    link = request.GET.get('link')
    title = request.GET.get('title')
    collect2 = models.Collect.objects.filter(user=a, news_title=title)
    if collect2:
        models.Collect.objects.filter(user=a, news_title=title).delete()
        if tag == 1:
            print(tag)
            return redirect('recommend.html')
        elif tag == 2:
            return redirect('yangshi.html')
        elif tag == 3:
            return redirect('renming.html')
        elif tag == 4:
            return redirect('xinghua.html')
        elif tag == 5:
            return redirect('qingnian.html')
        elif tag == 6:
            return redirect('zhongguo.html')
        elif tag == 7:
            return redirect('search.html')
        elif tag == 8:
            return redirect('usercollect.html')

    else:
        emotion = models.Newsparticiple.objects.get(news_title=title)
        models.Collect.objects.create(user=a, news_title=title, emotion_score=emotion.emotion_score)
        if tag == 1:
            return redirect('recommend.html')
        elif tag == 2:
            return redirect('yangshi.html')
        elif tag == 3:
            return redirect('renming.html')
        elif tag == 4:
            return redirect('xinghua.html')
        elif tag == 5:
            return redirect('qingnian.html')
        elif tag == 6:
            return redirect('zhongguo.html')
        elif tag == 7:
            return redirect('search.html')
        elif tag == 8:
            return redirect('usercollect.html')

    return redirect('recommend.html')


def alter(request):
    a = USER
    if request.method == 'POST':
        password = request.POST.get('username')
        password1 = request.POST.get('password')
        h = hashlib.md5()
        h.update(password.encode())
        mima = h.hexdigest()
        #print(username, password1)
        result_passw = re.compile(r'^(?=.*\d)(?=.*[a-zA-Z]).{6,20}$')  # 必须包含大写或小写字母和数字的组合，可以使用特殊字符，长度在6-20之间
        user = models.User.objects.get(username=a, password=mima)
        if user:
            if not result_passw.match(password1):
                msg = '密码必须包含字母和数字！'
                return render(request, 'alter.html', {'msg': msg})
            else:
                jiami = hashlib.md5()
                jiami.update(password1.encode())
                m = jiami.hexdigest()
                user.password = m
                user.save()
                return redirect('login.html')
        else:
            msg = '原密码不正确！'
            #print(msg)
            return render(request, 'alter.html', {'msg': msg})
    else:
        #print('111')
        return render(request, 'alter.html')
    return render(request, 'alter.html')


def Score(scan_score, collect_score):
    if scan_score == 0:
        return collect_score*0.6
    elif collect_score == 0:
        return scan_score*0.4
    else:
        return collect_score*0.6+scan_score*0.4

