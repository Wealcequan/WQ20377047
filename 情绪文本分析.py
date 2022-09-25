#20377047 温泉 第三周作业
import jieba
import csv
import re
import random
import pandas
import collections
import datetime
import math
import matplotlib.pyplot as plt
import numpy as np

#读取49999条数据
def readcsv(csv1):
    with open(csv1, 'r', encoding='utf-8', errors='ignore') as d:
        d_csv = csv.reader(d)
        datalist = []
        for row in d_csv:
            datalist.append(row)
        #将四列数据转化成列表单独储存
        datalocation = []
        datatext = []
        dataid = []
        datatime1 = []
        for i in range(2, len(datalist)):
            datalocation.append(datalist[i][1])
            datatext.append(datalist[i][2])
            dataid.append(datalist[i][3])
            datatime1.append(datalist[i][4])
    datatime=pandas.to_datetime(datatime1)
    return datalocation, datatext, dataid, datatime

#清洗数据
def clean(datatext):
    URL_REGEX = re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
    re.IGNORECASE)
    for i in range(len(datatext)):
        datatext[i] = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:| |$)", " ", datatext[i])  # 去除正文中的@和回复/转发中的用户名
        datatext[i] = re.sub(URL_REGEX, "", datatext[i])  # 去除url网址
#弹幕加工
def data_processing(datatext):
    #讲情绪词加入jiaba自定义词典
    jieba.setLogLevel(jieba.logging.INFO)
    jieba.load_userdict("anger.txt")
    jieba.load_userdict("disgust.txt")
    jieba.load_userdict("fear.txt")
    jieba.load_userdict("joy.txt")
    jieba.load_userdict("sadness.txt")
    #进行切词
    textdic = {}
    for i in range(len(datatext)):
        cutall = []
        cut1 = jieba.lcut(datatext[i])
        cut2 = ' '.join(cut1)
        cut3 = cut2.split()
        for j in range(len(cut3)):
            cutall.append(cut3[j])
        textdic[datatext[i]] = cutall
    #过滤停用词，返回以弹幕为keys，以分词结果为values的字典
    stopword = [line.strip() for line in open('stopwords_list.txt', encoding='UTF-8').readlines()]
    datatextdic = {}
    for i in range(len(datatext)):
        wordlist = []
        cutall = textdic[datatext[i]]
        for j in range(len(cutall)):
            if (cutall[j].strip() not in stopword) and (cutall[j] != ''):
                wordlist.append(cutall[j].strip())
        datatextdic[datatext[i]] = wordlist
    return datatextdic

#讲情绪词转化为字典
def readtxt(txt1):
    with open(txt1, "r", encoding='utf-8') as f:  # 打开文件
        data = f.read()  # 读取文件
        datal=data.split('\n')
    return datal

#传入分词结果和向量列表，按情绪有无计数
def emotionv(list1,vector):
    def counter(list2):
        nonlocal vector
        flag=0
        for i in range(len(list1)):
            if list1[i] in list2:
                flag=1
        vector.append(flag)
        return vector
    return counter

def emotion(listdic,anger,disgust,fear,joy,sadness):
    #调用闭包函数，形成情绪向量
    vector=[]
    f1=emotionv(listdic, vector)
    f1(anger)
    f1(disgust)
    f1(fear)
    f1(joy)
    f1(sadness)
    #统计情绪，多种情绪视为无情绪
    sumv = sum(vector)
    if sumv == 1:
        if vector[0]==1:
            st = 'anger'
        elif vector[1]==1:
            st = 'disgust'
        elif vector[2]==1:
            st = 'fear'
        elif vector[3]==1:
            st = 'joy'
        elif vector[4]==1:
            st = 'sadness'
    else:
        st = 'none'
    return vector,st

#时间分析,传入时间序列、分词列表、时间间隔（hour\week)、情绪词列表
def timepro(datatime,listdic,tinterval,anger,disgust,fear,joy,sadness):
    #得到状态列表
    stlist=[]
    for i in range(len(listdic)):
        vector=[]
        vector,state=emotion(listdic[i],anger,disgust,fear,joy,sadness)
        stlist.append(state)
    listhour=['0~1','1~2','2~3','3~4','4~5','5~6',\
              '6~7','7~8','8~9','9~10','10~11','11~12',\
              '12~13','13~14','14~15','15~16','16~17','17~18',\
              '18~19','19~20','20~21','21~22','22~23','23~24']
    listweek=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    #按传入的两种参数，得到一天内或一周内，不同时间段各种情绪所占比例
    if tinterval=='hour':
        #初始化列表
        angerlist=[0]*24
        disgustlist=[0]*24
        fearlist=[0]*24
        joylist=[0]*24
        sadnesslist=[0]*24
        emotionall=[0]*24
        for i in range(len(listdic)):
            #时间返回int，天然索引
            j=datatime[i].hour
            if stlist[i]=='anger':
                angerlist[j]+=1
                emotionall[j]+=1
            elif stlist[i]=='disgust':
                disgustlist[j]+=1
                emotionall[j]+=1
            elif stlist[i]=='fear':
                fearlist[j]+=1
                emotionall[j]+=1
            elif stlist[i]=='joy':
                joylist[j]+=1
                emotionall[j]+=1
            elif stlist[i]=='sadness':
                sadnesslist[j]+=1
                emotionall[j]+=1
        #emotionall列表储存了每个时间段的情绪词总数
        emolist=[]
        for i in range(24):
            #避免做除法时无法进行
            if emotionall[i]==0:
                emotionall[i]=1
            str1='anger='+('%.2f'%(angerlist[i]/emotionall[i]))+','\
                +'disgust='+('%.2f'%(disgustlist[i]/emotionall[i]))+','\
                +'fear='+('%.2f'%(fearlist[i]/emotionall[i]))+','\
                +'joy='+('%.2f'%(joylist[i]/emotionall[i]))+','\
                +'sadness='+('%.2f'%(sadnesslist[i]/emotionall[i]))
            emolist.append(str1)
        #形成时间对情绪状况的列表
        emodic={}
        for i in range(24):
            emodic[listhour[i]]=emolist[i]
    #同上，将条件由24小时改为7天
    elif tinterval=='week':
        angerlist=[0]*7
        disgustlist=[0]*7
        fearlist=[0]*7
        joylist=[0]*7
        sadnesslist=[0]*7
        emotionall=[0]*7
        for i in range(len(listdic)):
            j=datatime[i].weekday()
            if stlist[i]=='anger':
                angerlist[j]+=1
                emotionall[j]+=1
            elif stlist[i]=='disgust':
                disgustlist[j]+=1
                emotionall[j]+=1
            elif stlist[i]=='fear':
                fearlist[j]+=1
                emotionall[j]+=1
            elif stlist[i]=='joy':
                joylist[j]+=1
                emotionall[j]+=1
            elif stlist[i]=='sadness':
                sadnesslist[j]+=1
                emotionall[j]+=1
        emolist=[]
        for i in range(7):
            if emotionall[i]==0:
                emotionall[i]=1
            str1='anger='+('%.2f'%(angerlist[i]/emotionall[i]))+','\
                +'disgust='+('%.2f'%(disgustlist[i]/emotionall[i]))+','\
                +'fear='+('%.2f'%(fearlist[i]/emotionall[i]))+','\
                +'joy='+('%.2f'%(joylist[i]/emotionall[i]))+','\
                +'sadness='+('%.2f'%(sadnesslist[i]/emotionall[i]))
            emolist.append(str1)
        emodic={}
        for i in range(7):
            emodic[listweek[i]]=emolist[i]
    return emodic

#地点分析,传入位置序列、分词列表、中心点、情绪词列表
def locationpro(datalocation,listdic,beijing,anger,disgust,fear,joy,sadness):
    #计算距离储存在distance中
    locationlist=[]
    for i in range(len(listdic)):
        num= datalocation[0].strip('[]').split(',')
        num=[float(j) for j in num]
        locationlist.append(num)
    distance=[]
    for i in range(len(listdic)):
        d1=locationlist[i][0]-beijing[0]
        d2=locationlist[i][1]-beijing[1]
        d=math.sqrt(pow(d1,2)+pow(d2,2))
        distance.append(d)
    #计算每个弹幕的情绪
    stlist=[]
    for i in range(len(listdic)):
        vector=[]
        vector,state=emotion(listdic[i],anger,disgust,fear,joy,sadness)
        stlist.append(state)
    #进行绘图表示
    a=list(np.linspace(0.162,0.17,10))
    #按段储存每种情绪的数量
    angerlist=[]
    disgustlist=[]
    fearlist=[]
    joylist=[]
    sadnesslist=[]
    flag1=0.16
    flag2=0.162
    for i in range(10):
        #储存每段内，每种情绪的数量和总数量，计算比例
        angerl=[0]*10
        disgustl=[0]*10
        fearl=[0]*10
        joyl=[0]*10
        sadnessl=[0]*10
        emotionl=[0]*10
        for j in range(len(listdic)):
            if (distance[j]>=flag1) and (distance[j]<=flag2):
                if stlist[j]=='anger':
                    angerl[i]+=1
                    emotionl[i]+=1
                elif stlist[j]=='disgust':
                    disgustl[i]+=1
                    emotionl[i]+=1
                elif stlist[j]=='fear':
                    fearl[i]+=1
                    emotionl[i]+=1
                elif stlist[j]=='joy':
                    joyl[i]+=1
                    emotionl[i]+=1
                elif stlist[j]=='sadness':
                    sadnessl[i]+=1
                    emotionl[i]+=1
            if emotionl[i]==0:
                emotionl[i]=1
        angerlist.append(float('%.4f'%(angerl[i]/emotionl[i])))
        disgustlist.append(float('%.4f'%(disgustl[i]/emotionl[i])))
        fearlist.append(float('%.4f'%(fearl[i]/emotionl[i])))
        joylist.append(float('%.4f'%(joyl[i]/emotionl[i])))
        sadnesslist.append(float('%.4f'%(sadnessl[i]/emotionl[i])))
        flag1+=0.002
        flag2+=0.002
    #进行绘图
    plt.plot(a,angerlist,label='anger',linewidth=2)
    plt.plot(a,disgustlist,label='disguat',linewidth=2)
    plt.plot(a,fearlist,label='fear',linewidth=2)
    plt.plot(a,joylist,label='joy',linewidth=2)
    plt.plot(a,sadnesslist,label='sadness',linewidth=2)
    plt.xlabel("Distance",fontsize=14)
    plt.ylabel("Scale",fontsize=14)
    plt.axis([0.168, 0.17, 0, 1])
    plt.tick_params(axis='both', labelsize=14)
    plt.legend()
    plt.show()

def main():
    datalocation, datatext, dataid, datatime=readcsv("a.csv")
    clean(datatext)
    datatextdic=data_processing(datatext)
    anger=readtxt("anger.txt")
    disgust=readtxt("disgust.txt")
    fear=readtxt("fear.txt")
    joy=readtxt("joy.txt")
    sadness=readtxt("sadness.txt")
    #随机选取，返回其情绪和情绪向量
    index = random.randint(0,49999)
    vector,state=emotion(datatextdic[datatext[index]],anger,disgust,fear,joy,sadness)
    print(index)
    print(datatext[index])
    print(state)
    print(vector)
    #初始化两个参数，打印
    hour='hour'
    week='week'
    emodichour=timepro(datatime,list(datatextdic.values()),hour,anger,disgust,fear,joy,sadness)
    emodicweek=timepro(datatime,list(datatextdic.values()),week,anger,disgust,fear,joy,sadness)
    print(emodichour)
    print(emodicweek)
    #初始化城市中心
    beijing=[39.5420,116.2529]
    locationpro(datalocation,list(datatextdic.values()),beijing,anger,disgust,fear,joy,sadness)

if __name__=="__main__":
    main()