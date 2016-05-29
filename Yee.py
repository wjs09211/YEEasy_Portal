# -*- coding: utf-8 -*-
import urllib
import urllib2
from bs4 import BeautifulSoup
import json
import subprocess
import datetime
import os
from threading import Thread

from cStringIO import StringIO
from WindowFileParser import txt_parser, ppt_parser, docx_parser


def unquote_u(source):
    result = urllib.unquote(source)
    if '%u' in result:
        result = result.replace('%u','\\u').decode('unicode_escape')
    return result


def match_class(opener, account, class_name):
    _, class_table = get_class(opener, account)
    url = ""
    for key, value in class_table.iteritems():
        if unicode(key).split()[0] == class_name:
            url = value
    return url


def login(opener, account, password):
    # 登入網址
    url = 'https://portalx.yzu.edu.tw/PortalSocialVB/Login.aspx'
    try:
        html = urllib2.urlopen(url).read()
        html = BeautifulSoup(html, "html.parser")
        # post data
        data = {}
        data['Txt_UserID'] = account
        data['Txt_Password'] = password
        # asp.net特有的資料也要post過去
        data['__EVENTVALIDATION'] = html.find('input', {'id': '__EVENTVALIDATION'}).get('value')
        data['__VIEWSTATE'] = html.find('input', {'id': '__VIEWSTATE'}).get('value')
        data['ibnSubmit'] = '登入'
        # 編碼
        data = urllib.urlencode(data)
        # 使用有cookie的方式傳送
        info = opener.open(url, data).read()
        # <script>window.location='./FMain/DefaultPage.aspx?Menu=Default&LogExcute=Y';</script>
        # 代表登入成功
        if info.find("FMain/DefaultPage.aspx") != -1:
            return "login success"
        else:
            return "login fail"
    except:
        return "something error"


def check_work(opener, account):
    html = opener.open('https://portalx.yzu.edu.tw/PortalSocialVB/FMain/DefaultPage.aspx?Menu=Default').read()
    data = {'RequestType': "loadMyScheduleDataTable",
            'TheDay': "2016/05/26",
            'UserAccount': account}
    req = urllib2.Request('https://portalx.yzu.edu.tw/PortalSocialVB/FMain/DefaultPageRequest.ashx')
    req.add_header('Content-Type', 'application/json')
    response = opener.open(req, json.dumps(data)).read()
    response = json.loads(response)
    for r in response:
        if r["Title"].find(u"【作業】") != -1:
            end = int(r["EndDate"][6:-2])
            print r["Title"] + "  ", u"剩餘：",
            print (datetime.date.fromtimestamp(end/1000) - datetime.date.today()).days, u"天"
            # print r["URL"]


def get_class_table(info):
    info = BeautifulSoup(info, "html.parser")
    table = info.find('table', {'id': 'Table1'})  # 問卷的table
    trs = table.findAll('tr')
    schedule_table = []
    class_table = {}
    for tr in trs:
        row = []
        for td in tr:
            row.append(td.string)
            try:
                class_table[td.a.string] = td.a.get("href")
            except:
                pass
        schedule_table.append(row)
    return schedule_table, class_table


def get_class(opener, account, out_put=False):
    # 取得使用者帳號ID
    # html = opener.open('https://portalx.yzu.edu.tw/PortalSocialVB/FMain/DefaultPage.aspx?Menu=Default').read()
    # html = BeautifulSoup(html, "html.parser")
    # account = html.find('div', {'id': 'MainBar_divUserID'}).string

    # 模擬點集課表，為了得到session資料
    opener.open('https://portalx.yzu.edu.tw/PortalSocialVB/FMain/ClickMenuLog.aspx?type=App_&SysCode=S5')
    # 裡面有session資料
    html = opener.open('https://portalx.yzu.edu.tw/PortalSocialVB/IFrameSub.aspx').read()
    html = BeautifulSoup(html, "html.parser")

    # 取得 sessionID
    sessionID = html.find('input', {'id': 'SessionID'}).get('value')
    LangVersion = html.find('input', {'id': 'LangVersion'}).get('value')
    UseType = html.find('input', {'id': 'UseType'}).get('value')
    url = 'https://portal.yzu.edu.tw/VC2/FFB_Login.aspx?sys=STD_Schedule'  # 需要post檢查認證

    data = {'Account': account, 'SessionID': sessionID,
            'LangVersion': LangVersion, 'UseType': UseType}
    data = urllib.urlencode(data)

    info = opener.open(url, data).read()

    if out_put:
        print "Windows not support"
        # f = open("temp.txt", "w")
        # f.write(info)
        # f.close()
        # subprocess.call("perl perl/curriculum.pl temp.txt", shell=True)
        # subprocess.call("rm temp.txt", shell=True)

    return get_class_table(info)


def get_class_info(opener, account, class_name, count=100):
    url = match_class(opener, account, class_name)
    if url == "":
        print u"無此課程"
        return

    html = opener.open(url).read()
    html = BeautifulSoup(html, 'html.parser')
    tds = html.findAll('td', {'class': 'TDtitle'})
    if count > len(tds):
        count = len(tds)
    i = 0
    print "#"*50 + "\n"
    for td in tds:
        try:
            if td.a.string is not None:
                print td.a.string
                infoID = str(td.a.get("href"))
                start = infoID.find("(") + 1
                end = infoID.find(",")
                infoID = infoID[start:end]

                data = {
                    'ParentPostID': int(infoID),
                    'pageShow': 0
                }
                req = urllib2.Request('https://portalx.yzu.edu.tw/PortalSocialVB/FMain/PostWall.aspx/divParentInnerHtml')
                req.add_header('Content-Type', 'application/json')
                response = opener.open(req, json.dumps(data)).read()
                response = json.loads(response)
                response = BeautifulSoup(response['d'], "html.parser")
                div = response.find("div", {"id": "divPostBody"+infoID})
                if div.string is None:
                    # 下載項目可能要再做處理
                    print div.a.text
                    # print div.a.get("href")
                else:
                    print div.text
                print "\n" + "#"*50 + "\n"
                i += 1
                if i >= count:
                    break
        except:
            pass


def get_teach_material(opener, account, class_name, show=False):
    url = match_class(opener, account, class_name)
    if url == "":
        print u"無此課程"
        return
    opener.open(url)
    html = opener.open("https://portalx.yzu.edu.tw/PortalSocialVB/FMain/ClickMenuLog.aspx?type=Pag_Materials_S").read()
    # linux only
    # f = open("temp.txt", "w")
    # f.write(html)
    # f.close()
    html = BeautifulSoup(html, "html.parser")

    tds = html.findAll('td', {"class": ['record2', 'hi_line']})

    data = []
    temp = []
    for i, td in enumerate(tds):
        if i % 7 == 0:
            temp.append(td.text)
        if i % 7 == 4:
            temp.append(td.text)
        elif i % 7 == 1:
            temp.append("https://portalx.yzu.edu.tw/PortalSocialVB/" + td.a.get("href")[3:])
        elif i % 7 == 6:
            data.append(temp)
            temp = []

    if show:
        for i, d in enumerate(data):
            try:
                print str(i + 1) + ".", d[0], "\t", d[2]
                print
            except:
                pass
        # subprocess.call("perl perl/Teaching_material.pl temp.txt", shell=True)
        # subprocess.call("rm temp.txt", shell=True)

    return data


def down_load_file(opener, url, file_name, path="", show=False):
    if url == "":
        print "no file"
        return
    if not os.path.isdir(path):
        os.mkdir(path)
    file_name = unquote_u(file_name)
    file_data = opener.open(url).read()
    f = open(path + file_name, "wb")
    f.write(file_data)
    f.close()
    if show:
        print file_name, u"\t\tdownload finish"


def get_homework(opener, account, class_name, show=False):
    url = match_class(opener, account, class_name)
    if url == "":
        print u"無此課程"
        return

    opener.open(url)
    html = opener.open("https://portalx.yzu.edu.tw/PortalSocialVB/FMain/ClickMenuLog.aspx?type=Pag_Homework_S").read()
    html = BeautifulSoup(html, "html.parser")
    trs = html.findAll('tr', {"class": ['hi_line', 'record2']})
    i = 0
    data = []
    temp = []
    attachement_url = []
    for tr in trs:
        if i == 0:
            tds = tr.findAll('td')
            j = 0
            for td in tds:
                if j == 0 or j == 2 or j == 4 or j == 5 or j == 9 or j == 10:
                    temp.append(td.text)
                elif j == 3:
                    try:
                        url = "https://portalx.yzu.edu.tw/PortalSocialVB/" + td.a.get("href")[3:]
                        temp.append(url)
                        attachement_url.append(url)
                    except:
                        temp.append("")
                        attachement_url.append("")
                j += 1
                if j == 11:
                    j = 0
            i += 1
        elif i == 1:
            td = tr.find('td')
            description = ""
            for c in td.contents:
                if c.string is not None:
                    description += c.string + "\n"
            temp.append(description)
            data.append(temp)
            temp = []
            i = 0
    if show:
        for d in data:
            print "NO." + d[0], d[1]
            print "description:",  d[7],
            start = d[2].find("File_name=") + len("File_name=")
            end = d[2].find("&", start)
            print "Attachement:", d[2][start:end]
            print "Deadline:", d[3]
            print "File Uploaded:", d[4]
            print "Grad:", d[5]
            print "Comment:", d[6]
            print "#"*50

    return attachement_url


def upload_homework_file(opener, account, class_name, wk_id, file_name):
    url = match_class(opener, account, class_name)
    if url == "":
        print u"無此課程"
        return
    opener.open(url)
    html = opener.open("https://portalx.yzu.edu.tw/PortalSocialVB/FMain/ClickMenuLog.aspx?type=Pag_Homework_S").read()
    html = BeautifulSoup(html, "html.parser")

    from poster.encode import multipart_encode
    url = "https://portalx.yzu.edu.tw/PortalSocialVB/THom/HomeworkList.aspx?Menu=Hom"
    datagen, headers = multipart_encode({"FileUpload1": open(file_name, "rb"),
                                         'name': 'test3.txt',
                                         "wk_id": str(wk_id),
                                         "agree": "Upload_File",
                                         "__EVENTVALIDATION": html.find('input', {'id': '__EVENTVALIDATION'}).get('value'),
                                         "__VIEWSTATE": html.find('input', {'id': '__VIEWSTATE'}).get('value'),
                                        "__VIEWSTATEGENERATOR": html.find('input', {'id': '__VIEWSTATEGENERATOR'}).get('value'),
                                         "txt_Memo": ""})

    request = urllib2.Request(url, datagen, headers)
    urllib2.urlopen(request)


def find_key_word(opener, account, class_name, key):
    teach_material = get_teach_material(opener, account, class_name, show=False)
    if teach_material is None:
        return False
    if not os.path.isdir("material"):
        os.mkdir("material")
    path = "material/" + class_name + "/"
    if not os.path.isdir(path):
        os.mkdir(path)
    print 'down load file, please wait...'
    for ts in teach_material:
        url = ts[1]
        start = url.find("File_name=") + len("File_name=")
        end = url.find("&", start)
        file_name = unquote_u(url[start:end])
        if not os.path.isfile(path + file_name):
            down_load_file(opener, url, file_name, path)

        # if file_name.endswith('txt'):
        #     txt_parser(path + file_name, key)
        # elif file_name.endswith('ppt') or file_name.endswith('pptx'):
        #     ppt_parser(path + file_name, key)
        # elif file_name.endswith('docx'):
        #     docx_parser(path + file_name, key)
    docx_parser("test", key)

if __name__ == "__main__":
    print 'YEE'