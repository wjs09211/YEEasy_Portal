# -*- coding: utf-8 -*-
import urllib
import urllib2
from bs4 import BeautifulSoup

question_info = {}


def auto_fill_question(opener, account, value):

    opener.open('https://portalx.yzu.edu.tw/PortalSocialVB/FMain/ClickMenuLog.aspx?type=App_&SysCode=S5')  # 左邊的選單
    html = opener.open('https://portalx.yzu.edu.tw/PortalSocialVB/IFrameSub.aspx').read()  # 裡面有session資料
    html = BeautifulSoup(html, "html.parser")

    # 取得 sessionID
    sessionID = html.find('input', {'id': 'SessionID'}).get('value')
    LangVersion = html.find('input', {'id': 'LangVersion'}).get('value')
    UseType = html.find('input', {'id': 'UseType'}).get('value')

    data = {'Account': account, 'SessionID': sessionID,
            'LangVersion': LangVersion, 'UseType': UseType}
    data = urllib.urlencode(data)
    opener.open('https://portal.yzu.edu.tw/NewSurvey/NewLogin.aspx', data)  # 需要post檢查認證
    html = opener.open('https://portal.yzu.edu.tw/NewSurvey/std/F01_Questionnaire.aspx').read()  # 到了問卷頁面
    if html.find("查無待填問卷") != -1:
        print "查無待填問卷"
        return
    # 取得問卷網址
    get_question_info(html)
    # 填寫
    fill_questions(opener, value)
    return opener


def get_question_info(html):
    html = BeautifulSoup(html, "html.parser")
    html = html.find('table', {'class': 'table_1'})
    tds = html.findAll('td')
    for i, td in enumerate(tds):
        if i % 4 == 2:
            question_info[td.a.string] = td.a.get('href')


def fill_questions(opener, value):
    for class_name, url in question_info.iteritems():
        print class_name, "填寫完成"
        html = opener.open('https://portal.yzu.edu.tw/NewSurvey/std/' + url).read()  # 到問卷網頁
        html = BeautifulSoup(html, "html.parser")
        data = {}  # post_data
        # asp.net特有的資料要post過去
        data['__EVENTVALIDATION'] = html.find('input', {'id': '__EVENTVALIDATION'}).get('value')
        data['__VIEWSTATE'] = html.find('input', {'id': '__VIEWSTATE'}).get('value')
        data['btOK'] = '完成'

        table = html.find('table', {'id': 'tbQ'})  # 問卷的table
        inputs = table.findAll('input')  # 找到所有的input欄位
        for j, inpu in enumerate(inputs):
            name = inpu.get('name')  # 找到要post的欄位名稱
            data[name] = value

        data = urllib.urlencode(data)  # 編碼
        opener.open('https://portal.yzu.edu.tw/NewSurvey/std/' + url, data)  # 送資料
    print "完成"