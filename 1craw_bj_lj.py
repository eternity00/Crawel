import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
#'https://xa.lianjia.com/zufang'
#'https://bj.lianjia.com/zufang/xicheng/pg2/#contentList'
url='https://bj.lianjia.com/zufang'
#url='https://xa.lianjia.com/zufang'
#url='https://hanzhong.lianjia.com/zufang'
class Zufang:
    def __init__(self,url):
        #获取pg相关：
        rsp = requests.get(url)
        bs = BeautifulSoup(rsp.text, 'lxml') #如不写第二个参数，那么移植到其它平台可能默认格式不同
        content_pg = bs.find(class_='content__pg')
        self.pg_url=content_pg.get('data-url')#"/zufang/pg{page}/"
        self.pg_num =int(content_pg.get('data-totalpage'))
        print('{} zufang price:'.format(url.split('/')[2]))
        #print('pg_url:'+self.pg_url+'\t'+'pg_num:'+str(self.pg_num))
    def get_price(self,url):
        rsp = requests.get(url)
        #安装 lxml 解析器 pip install lxml 
        bs = BeautifulSoup(rsp.text, 'lxml') #如不写第二个参数，那么移植到其它平台可能默认格式不同
        #找到 header 元素列表
        price_all = bs.find_all(attrs={'class':"content__list--item-price"})#class 为关键字，加下划线以示区分
        #links_div = soup.find(class_='header')#class 为关键字，加下划线以示区分
        price_list=[]
        for i in price_all:
            pstr=i.get_text()
            price_list.append(int(pstr[0:pstr.find(' ')]))
        return price_list
    def get_allprice(self,url,n=10):#n为默认爬取页数
        assert(n>=1)
        #crawl_pg=n
        if self.pg_num>=2:
            newurl=''
            allprice_list=self.get_price(url)
            num = n if n<=self.pg_num else self.pg_num #取小
            for i in range(2,num+1):
                newurl=url+self.pg_url.format(page=i)
                allprice_list+=self.get_price(newurl)
            #print("That's all {} pages.".format(self.pg_num))
            print('Total is {} num price'.format(len(allprice_list)))
            print('{} pages have been crawled in all {} pages'.format(num,self.pg_num))
            return allprice_list
        else:
            print("Only one page.")
            return get_price(url)


#画柱状图
class PR(Enum):#PRA(界限值) 为PR1(间隔)的整数倍
    PR1=1000
    PRA=6000
def autolabel(rects):#画柱状图上的数字
    for rect in rects:
        height = rect.get_height() #<class 'numpy.int32'>
        plt.text(rect.get_x()+rect.get_width()/2.- 0.1, 0.2+height, height)
#plt.text 参数为 str int np. 等都可以
#rect.get_width() 0.8 <class 'numpy.float64'>
#rect.get_x() -0.4 <class 'numpy.float64'>
def numprice(li,low,high=None):#包括low，不包括hign，计算数量
    num=0
    if high!=None:
        if low>high:
            raise Exception('numprice error')#直接中断，无需return
        for i in li:
            if i>=low and i<high:
                num+=1
    else:
        for i in li:
            if i>=low:
                num+=1
    return num
#d默认为间隔，n为上限、超过的为一个柱状(n目前固定)
def pltprice(price,d=PR.PR1.value,n=PR.PRA.value): 
    assert(d in [i.value for i in PR])
    x_text = [str(i) for i in range(d,n+1,d)]#保存横坐标
    #+1 为 < 变成 <= 即包括 high，不包括low
    num_list = [numprice(price,int(i)-d+1,int(i)+1) for i in x_text]

    #显示6000+，(任意方式显示均可在这添加)
    x_text.append('{}+'.format(n))
    num_list += [numprice(price,n)]
    
    #tick_label 横坐标显示,替换第一个参数的值
    a=plt.bar(range(2,len(num_list)+2), num_list,color='rgb',tick_label=x_text)
    autolabel(a)
    plt.show()

zf=Zufang(url)
allprice=zf.get_allprice(url,5)#获取前5页的价格
pltprice(allprice)
#画图
'''
x=[i for i in range(0,len(allprice))]
y=allprice
plt.plot(x,y)
plt.show()
'''

