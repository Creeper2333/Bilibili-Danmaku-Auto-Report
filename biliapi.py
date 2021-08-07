import os
import requests
import re
import json
import sys
import xlwt
import time
import datetime
import xmltodict
from tkinter import *
from MyQR import myqr
from bs4 import BeautifulSoup
from PIL import Image, ImageTk

#bilibili options
def GetUsrLv(uid,sessdata):
    try:
        headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Host':'api.bilibili.com'
        }
        data={}
        data.update(mid=uid)
        cookie={}
        cookie.update(SESSDATA=sessdata)
        rslt=requests.get('http://api.bilibili.com/x/space/acc/info',headers=headers,
                      params=data,cookies=cookie,timeout=10)
        rsltJson=json.loads(rslt.text)
        return rsltJson['data']['level']
    except:
        return '-1'

def GetCid(bv):
    headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Host':'api.bilibili.com',
    'content-type':'application/x-www-form-urlencoded'
    }
    data={}
    data.update(bvid=bv)
    #print(data)
    rslt=requests.get('http://api.bilibili.com/x/player/pagelist',headers=headers,
                      params=data,timeout=10)
    print(rslt.text)
    rsltJson=json.loads('['+rslt.text+']')
    cid=rsltJson[0]['data'][0]['cid']
    return cid

def GetDanmaku(cid,sessdata):
    headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Host':'api.bilibili.com',
    'content-type':'application/x-www-form-urlencoded'
    }
    data={}
    data.update(oid=cid)
    rslt=requests.get('http://api.bilibili.com/x/v1/dm/list.so',headers=headers,
                      params=data,timeout=10)
    return rslt

def loginQr():
    print('打开b站客户端，扫码并确认后关闭扫码窗口即可。')
    headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Host':'passport.bilibili.com'
    }
    rslt=requests.get('http://passport.bilibili.com/qrcode/getLoginUrl',
                  headers=headers,timeout=10)
    urlJson=json.loads('['+rslt.text+']')
    url=urlJson[0]['data']['url']
    sp=os.getcwd()+'\\'
    myqr.run(words=url,
         version=1,
         level='M',
         save_dir=sp,
        )
    root=Tk()
    root.resizable(width='false', height='false')
    root.title='QrCode'
    label=Label(root,text='使用b站客户端扫码，扫完关掉窗口')
    label.grid(row=0,column=0)
    img=Image.open('qrcode.png')
    photo=ImageTk.PhotoImage(img)
    imglabel=Label(root,image=photo)
    imglabel.grid(row=1,column=0,columnspan=3)
    root.mainloop()
    return urlJson

def loginRslt(data):
    headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Host':'passport.bilibili.com'
    }
    postData={}
    postData.update(oauthKey=data[0]['data']['oauthKey'])
    #print(postData)
    loginInfo=requests.post('http://passport.bilibili.com/qrcode/getLoginInfo',
                           headers=headers,data=postData,timeout=10)
    #print(loginInfo.text)
    #print(str(loginInfo.cookies))
    return loginInfo

def Check(source):
    useless_chr=[
        '!','！',':','：','.',',','。','，','我','个'
    ]
    for chr in useless_chr:
        source=source.replace(chr,'')
    num=0
    try:
        num=int(source)
        if(re.match('233',str(num)).span()!=None):#str(num).replace('233','')==source
            return True
        elif(num%6 != 0):
            return False
        else:
            return True
    except:
        rule_f=open('rule.txt','r')
        rule=rule_f.readline()
        rule_f.close()
        result=re.search(rule,source)
        if(result.span()!=None):
            return True
        else:
            return False

def XmlToJson(dm_xml):
    try:
        #print(xml)
        convertJson=xmltodict.parse(dm_xml,encoding='utf-8')
        jsonRslt_=json.dumps(convertJson,indent=4)
        jsonRslt=json.loads(jsonRslt_)
        return jsonRslt
    except:
        print('Xml to json convert failed')

def reportdm(key,csrf,dmid,cid):
    headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Host':'api.bilibili.com',
    'content-type':'application/x-www-form-urlencoded'
    }
    c = {
    'csrf':csrf,
    'SESSDATA':key
    }
    postData={
    'csrf':csrf,
    'cid':cid,
    'dmid':dmid,
    'reason':'9'
    }
    rslt=requests.post('http://api.bilibili.com/x/dm/report/add',
                           cookies=c,headers=headers,data=postData,timeout=10)
    print(rslt.text)