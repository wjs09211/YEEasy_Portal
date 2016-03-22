# encoding=utf8
import base64


class UserInfo:
    def __init__(self):
        self.account = ""
        self.password = ""

    def create_base64_userInfo(self, account, password):
        account = base64.b64encode(account)
        password = base64.b64encode(password)
        f = open('userInfo', 'wb')
        f.write(account+'\n')
        f.write(password)

    def load_userInfo(self, file_name="userInfo"):
        try:
            f = open(file_name, 'rb')
            account, password = f.read().split()[0:2]
            self.account = base64.b64decode(account)
            self.password = base64.b64decode(password)
        except:
            print "no file"
