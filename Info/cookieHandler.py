# encoding=utf8
import cookielib
import urllib2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
cookie = None


def get_cookie(new):
    global cookie
    filename = 'cookie.txt'
    # 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
    if new:
        cookie = cookielib.MozillaCookieJar(filename)
    elif not new:
        cookie = cookielib.MozillaCookieJar()
        cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)

    opener = register_openers()
    opener.add_handler(urllib2.HTTPCookieProcessor(cookie))
    return opener
