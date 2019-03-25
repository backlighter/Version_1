import  requests
from  urllib import request
from bs4 import BeautifulSoup
import os
import json
import pymysql.cursors
import  time
ISOTIMEFORMAT='%Y-%m-%d %X'
connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='forum',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()
p_Image_Url=""
p_Owener=""
p_Describe=""
p_Tags=""
p_Date=""
def DataBaseLink(p_Image_Url,p_Owener,p_Describe,p_Tags):
    try:

        p_Date = time.strftime(ISOTIMEFORMAT, time.localtime())
    except Exception as e:
        print(e)
    sql = "insert into pic(" \
          "p_Image_Url," \
          "p_Owner," \
          "p_Describe," \
          "p_Tags," \
          "p_Date) values (%s,%s,%s,%s,%s);"
    param = [p_Image_Url, p_Owener, p_Describe, p_Tags, p_Date]
    cursor.execute(sql, param)
    # 事务
    connection.commit()
def DownLoadInmage(li,p_Owener,p_Describe,p_Tags): #下载每一个相册中的图片
    li_elss = soup.find(attrs={"data-blognickname":li.a.text}).find_all('div', class_='imgc')
    file = -1
    list=[]
    for li2 in li_elss:
        print(li2.img['src'])
        print(file)
        file += 1
        with request.urlopen(li2.img['src'])as di, open('./images/'+num+"/"+li.a.text+ '/image' + str(file) + '.jpg', 'wb')as wf:
            for l in di:
                wf.write(l)
            string="./images/"+num+"/"+li.a.text+ "/image" + str(file) + ".jpg"
            DataBaseLink(string,p_Owener,p_Describe,p_Tags)

    return
connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='forum',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

num=input("请输入要爬取的页数")
p_Tags=input("请输入要爬取的标签")
if not os.path.exists('./images/'+num):
    os.makedirs('./images/'+num)

url_net='http://www.lofter.com/tag/'+p_Tags+'/total?page='+num #更改页面切换网页
#url_net='http://www.lofter.com/tag/jk/total' #更改页面切换网页
res=requests.get(url_net,
                 headers={
                     'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'

                 })
res.encoding="utf-8"
#

soup=BeautifulSoup(res.text,'html.parser')
li_file_name=soup.find_all('div',class_="w-who")
li_file_isaym=soup.find_all('div',class_="cnt")
files=0
list2=[]
#创建文件夹和文件   文件夹名称  文件名称
try:
    for li4 in li_file_isaym:
        print(li4.p.text)

        list2.append(li4.p.text)

except Exception as e:
    print(e)
num3=0#用于计数
try:
    for li in li_file_name:

        dirname = os.path.join('./images/' + num, li.a.text)  # 创建文件夹名
        # dirname = os.path.join(li.a.text)

        print(li.a.text)
        # 创建目录
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        print(list2[num3]+"???")
        num3=num3+1
        DownLoadInmage(li,li.a.text,list2[num3],p_Tags)
except Exception as e:
    print(e)

