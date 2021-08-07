from biliapi import *
from crc32 import *


if __name__ == '__main__':
    if(input('选择登录方式：1是二维码，其它是手动输入SESSDATA和bili_jct。')=='1'):
        json_=loginQr()
        loginInfo=loginRslt(json_)
        print(str(loginInfo.cookies))
        print(loginInfo.text)
        loginJson=json.loads('['+loginInfo.text+']')
        try:
            loginMsg=loginJson[0]['message']
            print('登录操作失败,失败信息：'+loginMsg)
            SESSDATA='null'
            bili_jct='null'
            cid='null'
            input()
            os._exit(0)
        except:
            print('登录成功！')
            SESSDATA=loginInfo.cookies['SESSDATA']
            bili_jct=loginInfo.cookies['bili_jct']
            bvid=input('bv号:')
            cid=GetCid(bvid)
    else:
        try:
            SESSDATA=input('SESSDATA:')
            bili_jct=input('bili_jct:')
            bvid=input('bv号')
            cid=GetCid(bvid)
        except:
            input('请正确输入内容。')
            os._exit(0)

    xmlRslt=GetDanmaku(cid,SESSDATA)
    xmlRslt.encoding='utf-8'
    print('弹幕获取完成。')
    bs=BeautifulSoup(xmlRslt.text,'lxml')
    danmaku=bs.find_all('d')
    forbidden_dm_content=[]
    forbidden_usr=[]
    forbidden_dm_id=[]
    forbidden_level=[]
    for t in danmaku:
        #print(t)
        t_json=XmlToJson(str(t))
        print(t_json)
        data=t_json['d']['@p']
        d=data.split(',')
        word=t_json['d']['#text']
        if Check(word):
            forbidden_dm_content.append(word)
            usrid=caculate(d[6])
            forbidden_usr.append(usrid)
            forbidden_level.append(GetUsrLv(usrid,SESSDATA))
            forbidden_dm_id.append(d[7])

    f=xlwt.Workbook()
    tbl=f.add_sheet(bvid,datetime.datetime.now().strftime('%Y-%m-%d'))
    tbl.write(0,0,'弹幕内容')
    tbl.write(0,1,'弹幕发送者uid')
    tbl.write(0,2,'弹幕id')
    tbl.write(0,3,'用户等级')

    for i in range(len(forbidden_usr)):
        tbl.write(i+1,0,forbidden_dm_content[i])
        tbl.write(i+1,1,forbidden_usr[i])
        tbl.write(i+1,2,forbidden_dm_id[i])
        tbl.write(i+1,3,forbidden_level[i])

    f.save('danmaku.xls')
    #jsonRslt=XmlToJson(xmlRslt)
    #print(jsonRslt)
    for l in forbidden_dm_id:
        reportdm(SESSDATA,bili_jct,l,cid)
        time.sleep(1)
    input('完成，内容已输出至 danmaku.xls。')
