import requests
import re
import json
import openpyxl
import time,random
import sys,os

startshop=1000015633   #25/3中午运行到这里了
visitkey='45618802361819370'
run_times=10000
modikey=visitkey
ns = [[0 for x in range(3)] for y in range(1)]
j=0
runtimes=0
successTimes=0
tellme=0
blacktimes=0
startTime = time.time()

def create_xls(filename):
    if not os.path.isfile(filename):
        wb = openpyxl.Workbook()
        sht = wb.worksheets[0]
        sht["A1"] = '店铺'
        sht["B1"] = 'token'
        sht.title = "sheet1"
        wb.save(filename)
        wb2 = openpyxl.load_workbook(filename, keep_vba=True)
        wb2.save(filename)
def alter(file,old_str,new_str):
    file_data = ""
    replaced=0
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                replaced+=1
                if replaced==1: line = line.replace(old_str,new_str)
            file_data += line
    with open(file,"w",encoding="utf-8") as f:
        f.write(file_data)
create_xls('data.xlsm')
for i in range(startshop,startshop+run_times):
    try:
        runtimes+=1
        print (time.strftime('%H:%M:%S', time.localtime()) ,'正在运行第',i,'号店铺')
        time.sleep(int(2*random.random()))
        tellme=tellme+1
        url = "https://shop.m.jd.com/?shopId=" + str(i)
        # 模仿浏览器的headers
        headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 9; STF-AL10; HMSCore 6.4.0.311; GMSCore 19.6.29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 HuaweiBrowser/11.0.4.371 Mobile Safari/537.36",
            "Host" : "shop.m.jd.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'upgrade-insecure-requests': '1',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'cookie':'visitkey='+visitkey,
        }
        # 调用get方法，传入参数，返回结果集
        resp = requests.get(url,headers=headers,timeout=(30.05, 60.06))
        jsonD = json.dumps(resp.text)
        vid=r"\d+"
        a=re.search(vid,jsonD, re.M|re.I)
        if jsonD.find('Authorization Required')!=-1:
            print('黑了，偿试visitkey='+str(int(visitkey)+1)+'看看')
            visitkey=str(int(visitkey)+1)
            blacktimes +=1
            if blacktimes==30 : break
            continue
        if tellme % 20==0 :         #20次休息2-5秒
            print('休息几秒',jsonD[:40])
            time.sleep(int(5*random.random()+5))
        if a==None:
            continue
        url2='https://wq.jd.com/shopbranch/GetUrlSignDraw?channel=1&venderId='+str(a.group(0))
        header2={
            "user-agent": "Mozilla/5.0 (Linux; Android 9; STF-AL10; HMSCore 6.4.0.311; GMSCore 19.6.29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 HuaweiBrowser/11.0.4.371 Mobile Safari/537.36",
            "Host" : "wq.jd.com",
            "Accept": "*/*",
            "Accept-Language": "zh-cn",
            "Accept-encoding":"gzip, deflate",
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'referer': 'https://shop.m.jd.com/?shopId='+str(i),
            'cookie':'visitkey='+visitkey,
        }

        resp2 = requests.get(url2,headers=header2,timeout=(30.05, 60.06))
        json2 = json.dumps(resp2.text)
        tokenid=re.search("token\%3D[a-zA-Z0-9]+",json2, re.M|re.I)
        if json2.find('Authorization Required')!=-1:
            print('又黑了，偿试visitkey='+str(int(visitkey)+1)+'看看')
            visitkey=str(int(visitkey)+1)
            blacktimes +=1
            if blacktimes==30 : break
            continue
        if tokenid==None:
            if tellme % 33==0 :
                print('这是第',i,'个店铺',a.group(0),'还是没有')
            continue
        tokenid=tokenid.group(0)[-32:]
        print('发现有，存入'+str(i))
        shopaddr='https://shop.m.jd.com/?shopid='+str(i)

        ns[j]=[shopaddr,tokenid,time.strftime('%H:%M:%S', time.localtime())]
        successTimes+=1
        j=j+1
        data = openpyxl.load_workbook('data.xlsm',keep_vba=True)
        # 取第一张表
        table = data.worksheets[0]
        table = data.active
        nrows = table.max_row  # 获得行数
        ncolumns = table.max_column  # 获得列数
        for r in range(len(ns)):
            for c in range(len(ns[0])):
                table.cell(r + nrows+1, c + 1).value = ns[r][c]
        data.save('data.xlsm')
        j=0
        ns = [[0 for x in range(3)] for y in range(1)]
    except BaseException as e:
        print('停止，正在保存文件',e)
        break
#最后把上次执行到的店铺号写入文件中
alter("main.py", "startshop="+str(startshop), "startshop="+str(i))
alter("main.py", "visitkey='"+modikey+"'", "visitkey='"+visitkey+"'")
###############################
#记录运行时间
end_time = time.time()
run_time = round(end_time-startTime)
hour = run_time//3600
minute = (run_time-3600*hour)//60
second = run_time-3600*hour-60*minute
print (f'全部运行完毕，耗时：{hour}小时{minute}分钟{second}秒,共找了{runtimes}个店铺，找到目标{successTimes}个,更换身份{blacktimes}次')

