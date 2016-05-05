# encoding=utf8
import urllib
import urllib2
from bs4 import BeautifulSoup


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
    time_table=[]
    class_table={}
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


if __name__ == "__main__":
    print 'YEE'
