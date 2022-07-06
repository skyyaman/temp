#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/30 4:59 下午
# @File    : cookie.py
# @Project : jd_scripts
# @Desc    :
import json
from urllib.parse import urlencode
#import aiohttp
import base64
import requests
import urllib3
import os
import re
import time
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#fileurl='/jd/config/config.sh'
fileurl='dir/test.py'
AppWskey=[
    "pin=jd_TaPPlOeVwABN;wskey=;", ##157
    "pin=jd_RdmzkRlYKnFt;wskey=;", ##两个大黑号。也别管谁谁了
] 

def check_cloud():
    url_list = ['aHR0cDovL2FwaS5tb21vZS5tbC8=', 'aHR0cHM6Ly9hcGkubW9tb2UubWwv','aHR0cHM6Ly9hcGkuaWxpeWEuY2Yv'] 
    for i in url_list:
        url = str(base64.b64decode(i).decode())
        try:
            requests.get(url=url, verify=False, timeout=10)
        except Exception as err:
            #logger.debug(str(err))
            continue
        else:
            info = ['Default', 'HTTPS', 'CloudFlare']
            print(str(info[url_list.index(i)]) + " Server Check OK\n--------------------\n")
            return i
    print("\n云端地址全部失效, 请检查网络!")
    sys.exit(1)
url_t = check_cloud()
def cloud_info():
    url = str(base64.b64decode(url_t).decode()) + 'check_api'
    for i in range(3):
        try:
            headers = {"authorization": "Bearer Shizuku"}
            res = requests.get(url=url, verify=False, headers=headers, timeout=20).text
        except requests.exceptions.ConnectTimeout:
            #print("\n获取云端参数超时, 正在重试!" + str(i))
            time.sleep(1)
            continue
        except requests.exceptions.ReadTimeout:
            #print("\n获取云端参数超时, 正在重试!" + str(i))
            time.sleep(1)
            continue
        except Exception as err:
            #print("\n未知错误云端, 退出脚本!")
            #logger.debug(str(err))
            sys.exit(1)
        else:
            try:
                c_info = json.loads(res)
                #print('看看c_info:',c_info)
            except Exception as err:
                #print("云端参数解析失败")
                #logger.debug(str(err))
                sys.exit(1)
            else:
                return c_info

def getToken(wskey):  # 方法 获取 Wskey转换使用的 Token 由 JD_API 返回 这里传递 wskey

    try:  # 异常捕捉
        url = str(base64.b64decode(url_t).decode()) + 'api/genToken'  # 设置云端服务器地址 路由为 genToken
        header = {"User-Agent": ua}  # 设置 HTTP头
        params = requests.get(url=url, headers=header, verify=False, timeout=20).json()  # 设置 HTTP请求参数 超时 20秒 Json解析
    except Exception as err:  # 异常捕捉
        print("Params参数获取失败")
        return False, wskey  # 返回 -> False[Bool], Wskey
    headers = {
        'cookie': wskey,
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'charset': 'UTF-8',
        'accept-encoding': 'br,gzip,deflate',
        'user-agent': ua
    }  # 设置 HTTP头
    url = 'https://api.m.jd.com/client.action'  # 设置 URL地址
    data = 'body=%7B%22to%22%3A%22https%253a%252f%252fplogin.m.jd.com%252fjd-mlogin%252fstatic%252fhtml%252fappjmp_blank.html%22%7D&'  # 设置 POST 载荷
    try:  # 异常捕捉
        res = requests.post(url=url, params=params, headers=headers, data=data, verify=False,timeout=10)  # HTTP请求 [POST] 超时 10秒
        res_json = json.loads(res.text)  # Json模块 取值
        tokenKey = res_json['tokenKey']  # 取出TokenKey
    except Exception as err:  # 异常捕捉
        print("JD_WSKEY接口抛出错误 尝试重试 更换IP")  # 标准日志输出
        return False, wskey  # 返回 -> False[Bool], Wskey
    else:  # 判断分支
        #print('token::::::::',tokenKey)
        return appjmp(wskey, tokenKey)  # 传递 wskey, Tokenkey 执行方法 [appjmp]

def appjmp(wskey, tokenKey):  # 方法 传递 wskey & tokenKey
    #print('wskey:',wskey)
    #wskey = "pt_" + str(wskey.split(";")[0])  # 变量组合 使用 ; 分割变量 拼接 pt_
    if tokenKey == 'xxx':  # 判断 tokenKey返回值
        print(str(wskey) + ";疑似IP风控等问题 默认为失效\n--------------------\n")  # 标准日志输出
        return False, wskey  # 返回 -> False[Bool], Wskey
    headers = {
        'User-Agent': ua,
        'accept': 'accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'x-requested-with': 'com.jingdong.app.mall'
    }  # 设置 HTTP头
    params = {
        'tokenKey': tokenKey,
        'to': 'https://plogin.m.jd.com/jd-mlogin/static/html/appjmp_blank.html'
    }  # 设置 HTTP_URL 参数
    url = 'https://un.m.jd.com/cgi-bin/app/appjmp'  # 设置 URL地址
    try:  # 异常捕捉
        res = requests.get(url=url, headers=headers, params=params, verify=False, allow_redirects=False,timeout=20)  # HTTP请求 [GET] 阻止跳转 超时 20秒
        #print(res.cookies)
    except Exception as err:  # 异常捕捉
        print("JD_appjmp 接口错误 请重试或者更换IP\n")  # 标准日志输出
        return False, wskey  # 返回 -> False[Bool], Wskey
    else:  # 判断分支
        try:  # 异常捕捉
            res_set = res.cookies.get_dict()  # 从res cookie取出
            pt_key = 'pt_key=' + res_set['pt_key']  # 取值 [pt_key]
            pt_pin = 'pt_pin=' + res_set['pt_pin']  # 取值 [pt_pin]
            if "WSKEY_UPDATE_HOUR" in os.environ:  # 判断是否在系统变量中启用 WSKEY_UPDATE_HOUR
                jd_ck = str(pt_key) + ';' + str(pt_pin) + ';__time=' + str(time.time()) + ';'  # 拼接变量
            else:  # 判断分支
                jd_ck = str(pt_key) + ';' + str(pt_pin) + ';'  # 拼接变量
        except Exception as err:  # 异常捕捉
            print("JD_appjmp提取Cookie错误 请重试或者更换IP\n")  # 标准日志输出
            return False, wskey  # 返回 -> False[Bool], Wskey
        else:  # 判断分支
            if 'fake' in pt_key:  # 判断 pt_key中 是否存在fake
                print(str(wskey) + ";WsKey状态失效,有fake。。。\n")  # 标准日志输出
                return False, wskey  # 返回 -> False[Bool], Wskey
            else:  # 判断分支
                #print(str(wskey).split(';')[0].split('=')[1] + ":WsKey状态正常\n")  # 标准日志输出
                return True, jd_ck  # 返回 -> True[Bool], jd_ck

def ws_key_to_pt_key(pt_pin, ws_key):
    cookies = {
        'pin': pt_pin,
        'wskey': ws_key,
    }
    headers = {
        'user-agent': 'okhttp/3.12.1;jdmall;android;version/10.1.2;build/89743;screen/1080x2293;os/11;network/wifi;',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    #url = 'https://api.m.jd.com/client.action?functionId=genToken&clientVersion=10.1.2&build=89743&client=android' \
    #      '&d_brand=&d_model=&osVersion=&screen=&partner=&oaid=&openudid=a27b83d3d1dba1cc&eid=&sdkVersion=30&lang' \
    #      '=zh_CN&uuid=a27b83d3d1dba1cc&aid=a27b83d3d1dba1cc&area=19_1601_36953_50397&networkType=wifi&wifiBssid=&uts' \
    #      '=&uemps=0-2&harmonyOs=0&st=1630413012009&sign=ca712dabc123eadd584ce93f63e00207&sv=121'
    headers = {
        'pin': pt_pin,
        'cookie':ws_key,
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'charset': 'UTF-8',
        'accept-encoding': 'br,gzip,deflate',
        'user-agent': ua
    }
    url = 'https://api.m.jd.com/client.action'
    data = 'body=%7B%22to%22%3A%22https%253a%252f%252fplogin.m.jd.com%252fjd-mlogin%252fstatic%252fhtml%252fappjmp_blank.html%22%7D&'    
    response = requests.post(url, data=data, headers=headers, verify=False, timeout=10)
    data = json.loads(response.text)
    if data.get('code') != '0':
        return None
    token = data.get('tokenKey')
    url = data.get('url')
    session = requests.session()
    params = {
        'tokenKey': token,
        'to': 'https://plogin.m.jd.com/jd-mlogin/static/html/appjmp_blank.html'
    }
    url += '?' + urlencode(params)
    session.get(url, allow_redirects=True)
    for k, v in session.cookies.items():
        if k == 'pt_key':
             return v
    return None
    
if __name__ == '__main__':

    cloud_arg = cloud_info()
    ua = cloud_arg['User-Agent']
    lineNum = 0
    ##暂时不改配置文件，直接用本文件里的wskey
    with open(fileurl, 'r', encoding='UTF-8') as file:
        content = file.read()
    j=0
    print(f'共有{len(AppWskey)}个账号')
    for i in AppWskey:
        j=j+1
        return_staus,return_ck = getToken(i)
        print(return_staus,return_ck)
        if return_staus:
            pin=i.split(';')[0].split('=')[1]
            print("正在替换第",j,"个：",pin)
            p1="pt_key=[\S]+[\s]??pt_pin="+pin+";"    #+号不是连接，[\S]+表示多个非空字符 [\s]??表示0个或1个空格。晕
            content=re.sub(p1,return_ck, content, 0)
    with open(fileurl, 'w', encoding='UTF-8') as f:
        f.write(content)
