# encoding=utf8
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup


def login(opener, account, password):
    # 登入網址
    url = 'https://portalx.yzu.edu.tw/PortalSocialVB/Login.aspx'
    html = urllib2.urlopen(url).read()
    html = BeautifulSoup(html)
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


def get_class(opener, account):
    # 模擬點集課表，為了得到session資料
    opener.open('https://portalx.yzu.edu.tw/PortalSocialVB/FMain/ClickMenuLog.aspx?type=App_&SysCode=S5')
    # 裡面有session資料
    html = opener.open('https://portalx.yzu.edu.tw/PortalSocialVB/IFrameSub.aspx').read()
    html = BeautifulSoup(html)

    # 取得 sessionID
    sessionID = html.find('input', {'id': 'SessionID'}).get('value')
    LangVersion = html.find('input', {'id': 'LangVersion'}).get('value')
    UseType = html.find('input', {'id': 'UseType'}).get('value')
    url = 'https://portal.yzu.edu.tw/VC2/FFB_Login.aspx?sys=STD_Schedule'  # 需要post檢查認證

    data = {'Account': account, 'SessionID': sessionID,
            'LangVersion': LangVersion, 'UseType': UseType}
    data = urllib.urlencode(data)

    info = opener.open(url, data).read()
    return info

if __name__ == "__main__":
    print 'YEE'
