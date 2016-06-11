# -*- coding: utf-8 -*-
import os

from bs4 import BeautifulSoup

from Info import cookieHandler
from Info.Args import args
from method.AutoFillQuestion import auto_fill_question
from method.GoogleCalendar import calendar_insert
from method.Yee import login, get_class, get_class_info, get_teach_material, \
    down_load_file, get_homework, upload_homework_file, check_work, find_key_word, check_midtern_d, get_avg_score, get_range_score

import warnings
warnings.filterwarnings("ignore")

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
        check_midtern_d(opener, account)
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
# region-t className number
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
        if not os.path.isdir("material"):
            os.mkdir("material")
        data = get_teach_material(opener, account, args.teach_material[0], False)
        url = data[number - 1][1]
        start = url.find("File_name=") + len("File_name=")
        end = url.find("&", start)
        down_load_file(opener, url, url[start:end], 'material/' + args.teach_material[0] + '/',  show=True)
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
        if not os.path.isdir("homework"):
            os.mkdir("homework")
        data = get_homework(opener, account, args.homework[0], False)
        url = data[number]
        start = url.find("File_name=") + len("File_name=")
        end = url.find("&", start)
        down_load_file(opener, url, url[start:end], 'homework/' + args.homework[0] + '/', show=True)
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
# region -goo
elif args.google_calendar:
    schedule_table, class_table = get_class(opener, account)
    calendar_insert(schedule_table)
# endregion
# region -g
elif args.grade is not None:
    if args.average is not None:
        if len(args.average) == 0:
            grade = get_avg_score(opener, account)
            print u"學期總平均為: " + str(grade)
        elif len(args.average) == 1:
            try:
                grade = get_avg_score(opener, account, [args.average[0]])
                print u"第" + args.average[0][0:-2] + u"年 第" + args.average[0][-1:] + u"學期 平均為:" + str(grade)
            except:
                print u"輸入錯誤"
        else:
            print u"輸入錯誤"
    else:
        if len(args.grade) >= 1:
            number = 0
            try:
                number = int(args.grade[0])
            except:
                print 'first argument to "{' + args.grade[0] + '}" requires an integer'
                exit()
            if len(args.grade) == 1:
                get_range_score(opener, account, number)
            else:
                if args.grade[1] == u'up':
                    get_range_score(opener, account, number, True)
                elif args.grade[1] == u'down':
                    get_range_score(opener, account, number, False)
                else:
                    print 'second argument need \"up\" or \"down\"'
# endregion

# find_key_word(opener, account,"CS377", "test")
# datas = get_score(opener, account, ['104/1'])
# check_midtern_d(opener, account)
# get_avg_score(opener, account, ['102/2'])
# print get_current_semester()
# get_range_score(opener, account, 90)

