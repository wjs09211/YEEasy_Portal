# -*- coding: utf-8 -*-
import urllib
import urllib2
from bs4 import BeautifulSoup
import argparse
from Yee import login, get_class, get_class_info, get_class_book, down_load_file
from Info import cookieHandler
from Info.UserInfo import UserInfo
from AutoFillQuestion import auto_fill_question


account = ""


def check_cookie():
    global account
    html = opener.open('https://portalx.yzu.edu.tw/PortalSocialVB/FMain/DefaultPage.aspx?Menu=Default').read()
    if html.find("尚未登入") != -1:
        print "連線逾時，請重新登入"
        return False
    else:
        html = BeautifulSoup(html, "html.parser")
        account = html.find('div', {'id': 'MainBar_divUserID'}).string
        return True

parser = argparse.ArgumentParser(description='YEE')
parser.add_argument('-l', '--login', action='store_true', help='login')
parser.add_argument('-c', '--classs', action='store_true')
parser.add_argument('-cs', '--class_schedule', action='store_true')
parser.add_argument('-i', '--class_info', nargs="+")
parser.add_argument('-t', '--teach_material', nargs="+")
args = parser.parse_args()

# region login
if args.login:
    import getpass
    account = raw_input('account: ')
    pwd = getpass.getpass('password: ')
    opener = cookieHandler.get_cookie(True)
    info = login(opener, account, pwd)
    print info
    if info.find("請輸入使用者帳號密碼") != -1 or info.find("登入失敗") != -1 or info.find("異常") != -1 or info.find("fail") != -1:
        print u"登入失敗"
    else:
        cookieHandler.cookie.save(ignore_discard=True, ignore_expires=True)
    exit()
else:
    try:
        opener = cookieHandler.get_cookie(False)
    except:
        print u"請先登入"
        exit()

if not check_cookie():
    exit()
# endregions
if args.classs:
    schedule_table, class_table = get_class(opener, account)
    for rows in class_table:
        print rows.split()[0], rows.split()[2]
elif args.class_schedule:
    schedule_table, class_table = get_class(opener, account, True)
    # for rows in schedule_table:
    #     print rows
elif args.class_info is not None:
    if len(args.class_info) == 1:
        get_class_info(opener, account, args.class_info[0])
    elif len(args.class_info) == 2:
        get_class_info(opener, account, args.class_info[0], int(args.class_info[1]))

elif args.teach_material is not None:
    # 看教材
    if len(args.teach_material) == 1:
        get_class_book(opener, account, args.teach_material[0], True)
    # 下載教材
    elif len(args.teach_material) == 2:
        data = get_class_book(opener, account, args.teach_material[0], False)
        url = data[int(args.teach_material[1])][1]
        start = url.find("File_name=") + len("File_name=")
        end = url.find("&", start)
        down_load_file(opener, url, url[start:end])

# auto_fill_question(opener, account, 1)

