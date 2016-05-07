# encoding=utf8
import urllib
import urllib2
from bs4 import BeautifulSoup
import json


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
        return info
    except:
        return "fail"


def get_class_table(info):
    info = BeautifulSoup(info, "html.parser")
    table = info.find('table', {'id': 'Table1'})  # 問卷的table
    trs = table.findAll('tr')
    time_table = []
    class_table = {}
    for tr in trs:
        row = []
        for td in tr:
            row.append(td.string)
            try:
                class_table[td.a.string] = td.a.get("href")
            except:
                pass
        time_table.append(row)
    return time_table, class_table


def get_class(opener):
    # 取得使用者帳號ID
    html = opener.open('https://portalx.yzu.edu.tw/PortalSocialVB/FMain/DefaultPage.aspx?Menu=Default').read()
    html = BeautifulSoup(html, "html.parser")
    account = html.find('div', {'id': 'MainBar_divUserID'}).string

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

    return get_class_table(info)


def get_class_info(opener, class_name):
    _, class_table = get_class(opener)
    url = ""
    for key, value in class_table.iteritems():
        if unicode(key).split()[0] == class_name:
            url = value

    html = opener.open(url).read()
    html = BeautifulSoup(html, 'html.parser')
    tds = html.findAll('td', {'class': 'TDtitle'})
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
                print "#"*50
                print "#"*50
        except:
            pass


def get_class_book(opener, class_name):
    _, class_table = get_class(opener)
    url = ""
    for key, value in class_table.iteritems():
        if unicode(key).split()[0] == class_name:
            url = value
    # https://portalx.yzu.edu.tw/PortalSocialVB/FMain/ClickMenuLog.aspx?type=Pag_Materials_S
    opener.open(url)
    html = opener.open("https://portalx.yzu.edu.tw/PortalSocialVB/FMain/ClickMenuLog.aspx?type=Pag_Materials_S").read()
    html = BeautifulSoup(html, "html.parser")

    tds = html.findAll('td', {"class": ['record2', 'hi_line']})

    for td in tds:
        print td

    pass
if __name__ == "__main__":
    print 'YEE'
    # data = {
    #     'ids': [12, 3, 4, 5, 6]
    # }
    #
    # req = urllib2.Request('http://example.com/api/posts/create')
    # req.add_header('Content-Type', 'application/json')
    #
    # response = urllib2.urlopen(req, json.dumps(data))
