#20377047 温泉 第二周作业
#简单的弹幕文本分析任务
import string
import textwrap
import difflib
import collections
import random
import heapq
import bisect
import csv
import jieba
import wordcloud
import cv2

def main():
    pass

#读入文档并分词
def readcut(csv1):
    #截取前10000条弹幕的第一列
    with open(csv1,'rt', encoding='ANSI', errors='ignore') as d:
        d_csv=csv.reader(d)
        head=[column[0] for column in d_csv]
        headlist=list(head)
        cutall=[]
        for i in range(len(headlist)):
            cut1=jieba.lcut(headlist[i])
            cut2=' '.join(cut1)
            cut3=cut2.split()
            for j in range(len(cut3)):
                cutall.append(cut3[j])
    #返回弹幕列表和分词列表
    return headlist,cutall

#过滤停用词
def filter(cutall, stopword):
    wordlist=[]
    for i in range(len(cutall)):
        if (cutall[i].strip() not in stopword) and (cutall[i]!=''):
            wordlist.append(cutall[i].strip())
    return wordlist
#统计词频
def word_count(lis):
    count1=collections.Counter(lis)
    #返回词频字典
    return(count1)

#特征词筛选
def screen(dic1):
    dic2={}
    #筛选词频大于5的词
    for i in dic1:
        dic2[i]=dic1[i]
    for i in dic2:
        if dic1[i]<6:
            del dic1[i]
    return dic1
#特征集（0，1）向量表示
def vector(headlist,term):
    vectorlist={}
    key=term.keys()
    for i in headlist:
        list0=[0]*len(term)
        k=0
        for j in term.keys():
            if j in i:
                list0[k]=1
            k+=1
        list1=list0[:]
        vectorlist[i]=list1
    return vectorlist
#语义相似度
def randomchoose(vectorlist):
    length=len(vectorlist)
    random1=random.randint(0,length)
    keys=list(vectorlist.keys())
    danmu1=keys[random1]
    vec0=vectorlist[danmu1]
    dic1={}
    #计算距离
    for i in keys:
        num=vectorlist[i]
        dis=0
        for j in range(len(num)):
            dis+=abs(num[j]-vec0[j])
        dic1[i]=dis
    #排序，二维列表头部距离更近
    danmu=sorted(dic1.items(), key=lambda x: x[1],reverse=False)
    for k in range(len(dic1)):
        if danmu[k][0]==danmu1:
            continue
        else:
            danmu2=danmu[k][0]
            break
    print("随机选取的弹幕为：")
    print(danmu1)
    print("语义最相似的弹幕：")
    print(danmu2)
#（附加）可视化呈现(词云图)
def wordcloudp(count1):
    pic=wordcloud.WordCloud(width=600,height=600,\
                            background_color='white',\
                            font_path='msyh.ttc',\
                            max_words=50,\
                            max_font_size=80,\
                            min_font_size=10)
    wordcount=list(count1.keys())
    wordcountlist=[]
    for i in range(50):
        wordcountlist.append(wordcount[i])
    wordcountstr=' '.join(wordcountlist)
    pic.generate(wordcountstr)
    pic.to_file("文本分析词云图.png")

#主函数
if __name__ == '__main__':
    main()
    jieba.setLogLevel(jieba.logging.INFO)
    headlist,list1=readcut('danmuku1.csv')
    stopword = [line.strip() for line in open('stopwords_list.txt', encoding='UTF-8').readlines()]
    keyword=filter(list1,stopword)
    count1=word_count(keyword)
    term=screen(count1)
    vectorlist=vector(headlist,term)
    randomchoose(vectorlist)
    wordcloudp(count1)
