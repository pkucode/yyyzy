import requests
import json
import datetime

import os
from apscheduler.schedulers.blocking import BlockingScheduler

###############################一下两部分参考了pku_epidemic 项目

## Part I 必需填写

sid = ""  # 学号
pwd = ""  # 密码
heath_status = "健康"  # 疫情诊断

###############################

## Part II 下面的内容依照个人情况填写。

### 省市区的编号格式 与 身份证前六位的编码格式是对应的，

### 可以百度“xx省xx市xx区 身份证号码前六位” 来获得。
### 如北京市海淀区 身份证号码前六位 为 110108
### 则省编号 = "11"， 市编号 = "01" 区编号 = "08".

mydata = {
        "xh": sid,
        "sfhx": "",
        "hxsj": "",  # 回校时间，格式为“20200409 170200” 2020年4月9日17点02分00秒
        "cfdssm": "",  # 出发地省编号
        "cfddjsm": "",  # 出发地市编号
        "cfdxjsm": "",  # 出发地区编号
        "sflsss": "",  # 是否留宿宿舍 (y/n)
        "sfcx": "",  # 是否出校 (y/n)

        # 不在校需填写：
        "dqszdxxdz": "",  # 当前所在地详细地址
        "dqszdsm": "",  # 当前所在地省编号
        "dqszddjsm": "",  # 当前所在地市编号
        "dqszdxjsm": "",  # 当前所在地区编号
        #
        # "sfqwhb14": "n",  # 14日内是否途径湖北或前往湖北 (y/n)
        # "sfjchb14": "n",  # 14日内是否接触过来自湖北地区的人员 (y/n)
        # "sfqwjw14": "n",  # 14日内是否有境外旅居史 (y/n)
        # "sfjcjw14": "n",  # 14日内是否接触过境外人员 (y/n)
        "sfmjqzbl":"n",
        "sfmjmjz":"n",
        "sfxfd":"n",
        "sfxfd_jr":"n",
        "hsjcjg":"n",
        "jjgcsj":"n",
        "sfzgfxdq":"n",


        "jrtw": "37",  # 今日体温（如"36.8")
        "sfczzz": "n",  # 是否存在病症
        "jqxdgj": "",  # 行动轨迹
        "qtqksm": "",  # 其他情况说明
        "tbrq": datetime.datetime.now().strftime("%Y%m%d"),  # 填报日期，自动生成
        "yqzd": heath_status,  # 疫情诊断

        # 下面不用管

        "dwdzxx": "",
        "dwjd": "",
        "dwwd": "",
        "sfdrfj": "",
        "chdfj": "",
        "simstoken": "",
        "jkm":""

    }


########################################


def auto():
    sess = requests.Session()
    portal = "https://portal.pku.edu.cn/portal2017/"
    pp = eval(str(sess.get(portal).headers))

    preurl = """https://iaaa.pku.edu.cn/iaaa/oauth.jsp?appID=portal2017&appName=%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6%E6%A0%A1%E5%86%85%E4%BF%A1%E6%81%AF%E9%97%A8%E6%88%B7%E6%96%B0%E7%89%88&redirectUrl=https://portal.pku.edu.cn/portal2017/ssoLogin.do"""
    prer = eval(str(sess.get(preurl).headers))
    # print(prer)
    portal_url = "https://iaaa.pku.edu.cn/iaaa/oauthlogin.do"
    login_data = {"appid": "portal2017", "userName": sid, "password": pwd, "randCode": "",
                  "smsCode": "",
                  "otpCode": "",
                  "redirUrl": "https://portal.pku.edu.cn/portal2017/ssoLogin.do"}
    r = sess.post(portal_url, login_data)
    token = json.loads(r.text)['token']
    # print(token)

    ssoLogin_url = "https://portal.pku.edu.cn/portal2017/ssoLogin.do?token=" + token
    res = sess.get(ssoLogin_url)
    # print(res.text)

    ep_url = "https://portal.pku.edu.cn/portal2017/util/appSysRedir.do?appId=epidemic"
    r = sess.get(ep_url)
    # print(r.text)

    link0 = "https://portal.pku.edu.cn/portal2017/account/insertUserLog.do?portletId=epidemic&portletName=%E7%87%95%E5%9B%AD%E4%BA%91%E6%88%98%E2%80%9C%E7%96%AB%E2%80%9D"
    r = sess.get(link0)
    # print(r.headers)

    Tb_url = "https://ssop.pku.edu.cn/stuAffair/edu/pku/stu/sa/jpf/yqfk/stu/saveMrtb.do"
    r = sess.post(Tb_url, data=mydata)
    b=r.text
    if r.json()["success"]==True:
            print("填写成功")

    else:
            print("填写失败")

   

scheduler = BlockingScheduler()

#每天凌晨零点自动填写，前提是程序一直运行
scheduler.add_job(auto, 'cron', day_of_week='0-6', hour=0,minute=0)

scheduler.start()
