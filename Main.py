# -*- coding: utf-8 -*-
import urllib
import urllib2
from bs4 import BeautifulSoup
import argparse
from Yee import login, get_class, get_class_info, get_teach_material, \
    down_load_file, get_homework, upload_homework_file, check_work, find_key_word
from Info import cookieHandler
from Info.UserInfo import UserInfo
from AutoFillQuestion import auto_fill_question

account = ""


def check_cookie():
    global account
    html = opener.open('https://portalx.yzu.edu.tw/PortalSocialVB/FMain/DefaultPage.aspx?Menu=Default').read()
    if html.find("尚未登入") != -1 or html.find("異常") != -1:
        print u"連線逾時，請重新登入"
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
parser.add_argument('-hw', '--homework', nargs="+")
parser.add_argument('-a', '--auto', type=int)
parser.add_argument('-f', '--find', nargs=2)
args = parser.parse_args()

# region login
if args.login:
    import getpass

    account = raw_input('account: ')
    pwd = getpass.getpass('password: ')
    opener = cookieHandler.get_cookie(True)

    info = login(opener, account, pwd)

    if info.find("請輸入使用者帳號密碼") != -1 or info.find("登入失敗") != -1 or info.find("異常") != -1 or info.find("fail") != -1:
        print u"登入失敗"
    else:
        cookieHandler.cookie.save(ignore_discard=True, ignore_expires=True)
        check_work(opener, account)
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

# region-c
if args.classs:
    schedule_table, class_table = get_class(opener, account)
    for rows in class_table:
        print rows.split()[0], rows.split()[2]
# endregion
# region-cs
elif args.class_schedule:
    schedule_table, class_table = get_class(opener, account, True)
# endregion
# region-i className number
elif args.class_info is not None:
    if len(args.class_info) == 1:
        get_class_info(opener, account, args.class_info[0])
    elif len(args.class_info) == 2:
        number = 0
        try:
            number = int(args.class_info[1])
        except:
            print 'second argument to "{' + args.class_info[1] + '}" requires an integer'
            exit()
        get_class_info(opener, account, args.class_info[0], number)
# endregion
# region-t number
elif args.teach_material is not None:
    # 看教材
    if len(args.teach_material) == 1:
        get_teach_material(opener, account, args.teach_material[0], True)
    # 下載教材
    elif len(args.teach_material) == 2:
        number = 0
        try:
            number = int(args.teach_material[1])
        except:
            print 'second argument to "{' + args.teach_material[1] + '}" requires an integer'
            exit()
        data = get_teach_material(opener, account, args.teach_material[0], False)
        url = data[number - 1][1]
        start = url.find("File_name=") + len("File_name=")
        end = url.find("&", start)
        down_load_file(opener, url, url[start:end], show=True)
# endregion
# region-hw classname number file_name
elif args.homework is not None:
    if len(args.homework) == 1:
        get_homework(opener, account, args.homework[0], True)
    elif len(args.homework) == 2:
        number = 0
        try:
            number = int(args.homework[1]) - 1
        except:
            print 'second argument to "{' + args.homework[1] + '}" requires an integer'
            exit()
        data = get_homework(opener, account, args.homework[0], False)
        url = data[number]
        start = url.find("File_name=") + len("File_name=")
        end = url.find("&", start)
        down_load_file(opener, url, url[start:end], show=True)
    elif len(args.homework) == 3:
        number = 0
        try:
            number = int(args.homework[1])
        except:
            print 'second argument to "{' + args.homework[1] + '}" requires an integer'
            exit()

        upload_homework_file(opener, account, args.homework[0], number, args.homework[2])
        print u"上傳成功"
# endregion
# region-a
elif args.auto is not None:
    auto_fill_question(opener, account, args.auto)
# endregion
# region -f
elif args.find is not None:
    find_key_word(opener, account, args.find[0], args.find[1])
# endregion

