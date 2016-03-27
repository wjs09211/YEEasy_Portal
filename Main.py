# encoding=utf8
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
from Yee import login, get_class
from Info import cookieHandler
from Info.UserInfo import UserInfo
from AutoFillQuestion import AutoFillQuestion

opener = cookieHandler.opener
user = UserInfo()
user.create_base64_userInfo('account', 'password')
user.load_userInfo()

info = login(opener, user.account, user.password)
print info
if info.find("請輸入使用者帳號密碼") != -1 or info.find("登入失敗") != -1 or info.find("異常") != -1 or info.find("fail") != -1:
    print "登入失敗"
    exit()
info = get_class(opener, user.account)
AutoFillQuestion(opener, user.account, 1)

cookieHandler.cookie.save(ignore_discard=True, ignore_expires=True)
