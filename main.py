import requests
import json
import datetime
# from datetime import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler


def auto():
    sid = ""  # 学号
    pwd = ""  # 密码
    heath_status = "健康"  # 疫情诊断

    mydata = {
        "xh": sid,
        "sfhx": "y",
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

        "sfqwhb14": "n",  # 14日内是否途径湖北或前往湖北 (y/n)
        "sfjchb14": "n",  # 14日内是否接触过来自湖北地区的人员 (y/n)
        "sfqwjw14": "n",  # 14日内是否有境外旅居史 (y/n)
        "sfjcjw14": "n",  # 14日内是否接触过境外人员 (y/n)

        "jrtw": "37",  # 今日体温
        "sfczzz": "n",  # 是否存在病症
        "jqxdgj": "",  # 行动轨迹
        "qtqksm": "",  # 其他情况说明
        "tbrq": datetime.datetime.now().strftime("%Y%m%d"),  # 填报日期，自动生成
        "yqzd": heath_status,  # 疫情诊断

        # 下面的不知道有什么用

        "dwdzxx": "",
        "dwjd": "",
        "dwwd": "",
        "sfdrfj": "",
        "chdfj": "",
        "simstoken": "",
        "jkm":""

    }
    sess = requests.Session()

    portal_url = "https://iaaa.pku.edu.cn/iaaa/oauthlogin.do"
    login_data = {'appid': "portal2017", 'userName': sid, 'password': pwd,
                  'redirUrl': 'https://portal.pku.edu.cn/portal2017/ssoLogin.do'}
    r = sess.post(portal_url, login_data)
    token = json.loads(r.text)['token']
    # print(token)

    ssoLogin_url = "https://portal.pku.edu.cn/portal2017/ssoLogin.do?token=" + token
    res = sess.get(ssoLogin_url)
    # print(res)
    ep_url = "https://portal.pku.edu.cn/portal2017/util/appSysRedir.do?appId=epidemic"
    r = sess.get(ep_url)
    # print(r.text)
    link0 = "https://portal.pku.edu.cn/portal2017/account/insertUserLog.do?portletId=epidemic&portletName=%E7%87%95%E5%9B%AD%E4%BA%91%E6%88%98%E2%80%9C%E7%96%AB%E2%80%9D"
    r = sess.get(link0)
    # print(r.text)
    Tb_url = "https://ssop.pku.edu.cn/stuAffair/edu/pku/stu/sa/jpf/yqfk/stu/saveMrtb.do"
    r = sess.post(Tb_url, data=mydata)
    if r.json()["success"]==True:
       print("填写成功")
      
    else:
       print("失败")
    
   



scheduler = BlockingScheduler()

scheduler.add_job(auto, 'cron', day_of_week='0-6', hour=0,minute=0)#每天0:00自动填写

scheduler.start()



