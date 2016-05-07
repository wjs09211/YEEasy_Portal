# encoding=utf8
import urllib
import urllib2
from bs4 import BeautifulSoup
import argparse
from Yee import login, get_class, get_class_info, get_class_book
from Info import cookieHandler
from Info.UserInfo import UserInfo
from AutoFillQuestion import AutoFillQuestion


def check_cookie():
    html = opener.open('https://portalx.yzu.edu.tw/PortalSocialVB/FMain/DefaultPage.aspx?Menu=Default').read()
    if html.find("尚未登入") != -1:
        print "連線逾時，請重新登入"
        return False
    else:
        return True

parser = argparse.ArgumentParser(description='YEE')
parser.add_argument('-l', '--login', nargs=2)
parser.add_argument('-ct', '--class_timetable', action='store_true')
args = parser.parse_args()

if args.login is not None:
    opener = cookieHandler.get_cookie(True)
    info = login(opener, args.login[0], args.login[1])
    print info
    if info.find("請輸入使用者帳號密碼") != -1 or info.find("登入失敗") != -1 or info.find("異常") != -1 or info.find("fail") != -1:
        print "登入失敗"
    else:
        cookieHandler.cookie.save(ignore_discard=True, ignore_expires=True)
    exit()
else:
    try:
        opener = cookieHandler.get_cookie(False)
    except:
        print "請先登入"
        exit()

if not check_cookie():
    exit()

# time_table, class_table = get_class(opener)
# print class_table
# get_class_info(opener, "CS362")
get_class_book(opener, "CS362")
# AutoFillQuestion(opener, 1)

