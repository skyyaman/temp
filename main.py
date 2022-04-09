##这个版本用在本地端。结果放在txt文件中
import requests
import re
import json
import openpyxl
import time,random
import sys,os

startshop=1000137698 #25/3中午运行到这里了 1000094421  1000128488
visitkey='11353796670241060'
run_times=20000
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
def write_txt(filename,txt):
    with open(filename,"a") as f:
        f.write(txt)
def finalTime(ft):  #记录截止时间
    now=int(re.match('[0-9]{10}',str(ft)).group(0))
    timeArray = time.localtime(now)
    finnalTime = time.strftime("%m-%d-%H:%M:%S", timeArray)
    return finnalTime
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
def findRuleList(string,listname):
    rulelist=[]
    infor=''
    everyday=0
    rulelist=json.loads(string).get('data').get(listname)
    days=0
    #print(rulelist)
    if rulelist!=None:
        #for ax in range(len(rulelist)):
        for ax in rulelist:
            days=ax.get('level')     #每份奖励的天数
            #days=rulelist[0].get('level')
            prizelist=ax.get('prizeList')   #每份奖励的详细规则列表
            for k in prizelist:
                if (k.get('type')==4):   #type是4是豆子 14是红包
                    if days==0: #每天奖励
                        infor=infor+f'每天：{int(k.get("discount"))},'
                    else:
                        infor=infor+f'{days}-{int(k.get("discount"))},'
                    everyday=everyday+k.get("discount")
                    #daycount=days
                if (k.get('type')==14):
                    infor=infor+f'{days}-{k.get("discount")/100}元红包,'
    
    if days!=0: everyday=str(round(everyday/days,2))
    return(infor,everyday)

write_txt('log/'+str(time.strftime('%m-%d', time.localtime()))+'.txt',str(time.strftime('%H:%M:%S', time.localtime()))+':开始'+str(startshop)+'！\n')

for i in range(startshop,startshop+run_times):
    #time.sleep(0)
    try:
        runtimes+=1
        tellme=tellme+1
        url = "https://shop.m.jd.com/?shopId=" + str(i)
        
        # 模仿浏览器的headers
        headers = {
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'accept-encoding': 'gzip, deflate,br',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie':'visitkey='+visitkey,
        }
        # 调用get方法，传入参数，返回结果集
        resp = requests.get(url,headers=headers,timeout=(30.05, 60.06))
        jsonD = json.dumps(resp.text)
        #print (jsonD)
        vid='\<title\>([\S\s]*?)\<\/title\>'
        vid=r"\d+"
        a=re.search(vid,jsonD, re.M|re.I)
        b=re.search('(?<=title\>).*(?=</title)',jsonD, re.M|re.I)
        dptitle=b[0].replace(' ','').encode('latin-1').decode('unicode_escape').replace('\r\n','')
        if dptitle=='京东购物' or dptitle=='店铺关店页':continue
        if b[0]!=-1:print(f'{time.strftime("%m-%d-%H:%M:%S", time.localtime())}:正在检查{dptitle}{i}中..')
        if jsonD.find('Authorization Required')!=-1:
            print('黑了，偿试visitkey='+str(int(visitkey)+1)+'看看')
            visitkey=str(int(visitkey)+1)
            blacktimes +=1
            if blacktimes==30 : break
            continue
        if tellme % 20==0 :         #20次休息2-5秒
            #print('休息几秒',jsonD[:40])
            time.sleep(int(5*random.random()+5))
        
        if a==None: continue
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
        #print (a)
        if tokenid==None:
            if tellme % 1000==0 :
                logging=str(time.strftime('%H:%M:%S', time.localtime()))+':第'+str(i)+'个店铺,还是没有\n'
                write_txt('log/'+str(time.strftime('%m-%d', time.localtime()))+'.txt',logging)
            continue
        tokenid=tokenid.group(0)[-32:]
        print(f'***************发现有，检查数据中{i}****************')
        shopaddr='https://shop.m.jd.com/?shopid='+str(i)

        url3='https://api.m.jd.com/api?appid=interCenter_shopSign&t=1648774694000&loginType=2&functionId=interact_center_shopSign_getActivityInfo&body={%22token%22:%22'+tokenid+'%22,%22venderId%22:%22%22}&jsonp=jsonp1000'
        header3={
            'accept':'*/*',
            'accept-encoding': 'gzip, deflate, br',
            'user-agent': 'jdapp;iPhone;10.4.4;;;M/5.0;appBuild/167991;jdSupportDarkMode/0;ef/1;ep/%7B%22ciphertype%22%3A5%2C%22cipher%22%3A%7B%22ud%22%3A%22CzOzCzc0YwVtDwHuDJuyY2GyEJC0EJG5ZNCyYtK3CJU0YzU3YtCyYm%3D%3D%22%2C%22sv%22%3A%22CJCkCy4n%22%2C%22iad%22%3A%22HJC0Dtq0C0OjENKzGy00HJHNBJrPGJCjHtPLDzLPDUSmDJHL%22%7D%2C%22ts%22%3A1648774693%2C%22hdid%22%3A%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw%3D%22%2C%22version%22%3A%221.0.3%22%2C%22appname%22%3A%22com.360buy.jdmobile%22%2C%22ridx%22%3A-1%7D;Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1;',
            'accept-language': 'zh-cn',
            'referer': 'https://h5.m.jd.com/babelDiy/Zeus/2PAAf74aG3D61qvfKUM5dxUssJQ9/index.html?token=DFBDE9D4A0EF038284396FDA8535D20C&sid=4c8be78390c78d263a9486e98dcacafw&un_area=19_1666_1669_52081',
            'cookie':'visitkey='+visitkey,
        }

        resp3 = requests.get(url3,headers=header3,timeout=(30.05, 60.06))
        json3 = json.dumps(resp3.text)
        res='(?<=\().*(?=\))'
        jsonE=re.search(res,json3,re.M|re.I).group(0).replace('\\','')
        infor=''
        everyday=0
        infor=findRuleList(jsonE,'prizeRuleList')[0]+findRuleList(jsonE,'continuePrizeRuleList')[0]

        if(infor==''):
            print('有活动，但是不是豆子红包，跳过继续下一个店铺。')
            continue
        else:
            print('*************OK，找到一个，下面开始分析奖励并写入********************')
            infor=infor+'结束时间：'+finalTime(json.loads(jsonE).get('data').get('endTime'))+b[0].replace(' ','').encode('latin-1').decode('unicode_escape').replace('\r\n','')
            if everyday!=0: infor=infor+';'+str(everyday)
        ns[j]=[shopaddr,tokenid,time.strftime('%H:%M:%S', time.localtime())]
        successTimes+=1
        j=j+1

        temp=str(time.strftime('%m-%d-%H:%M:%S', time.localtime()))+';'+ns[0][0] +";'"+str(tokenid)+"',//"+infor+';'+findRuleList(jsonE,'continuePrizeRuleList')[1]+'\n'
        write_txt('data.txt',temp)
        j=0
        temp=''
        ns = [[0 for x in range(3)] for y in range(1)]
    except BaseException as e:
        print('停止，正在保存文件',e)
        logging=str(time.strftime('%H:%M:%S', time.localtime()))+f':出现错误\n'+f'{e}'
        write_txt('log/'+str(time.strftime('%m-%d', time.localtime()))+'.txt',logging)
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
logging=str(time.strftime('%H:%M:%S', time.localtime()))+f':全部运行完毕，耗时：{hour}小时{minute}分钟{second}秒,共找了{runtimes}个店铺，找到目标{successTimes}个,更换身份{blacktimes}次\n'
write_txt('log/'+str(time.strftime('%m-%d', time.localtime()))+'.txt',logging)
