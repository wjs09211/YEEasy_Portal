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
# user.create_base64_userInfo('account', 'password')
user.load_userInfo()


_ = login(opener, user.account, user.password)

_ = get_class(opener, user.account)
AutoFillQuestion(opener, user.account, 1)

cookieHandler.cookie.save(ignore_discard=True, ignore_expires=True)
