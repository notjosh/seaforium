import requests
import lxml
import time
import json

from urlparse import urlparse
from lxml import html

# todo: I suppose refactoring YayAPIClient and YayClient to share code would make sense. yrmom.
#       at this point, the only real difference is '?format=json'. if that remains the case in future
#       let's merge!
class YayAPIClient:

    def __init__(self, options):
        self.options = options

    @staticmethod
    def post_thread(opts, cookies, cat, subject, content):
        data = {
            "category[]": cat,
            "content": content,
            "subject": subject
        }
        return YayAPIClient.time_req(opts, 'post', 'newthread', data, cookies)

    @staticmethod
    def time_req(opts, method, path, data=[], cookies=None):
        if ("timer_file" in opts):
            time0 = time.time()
            ret = requests.request(method, opts['url'] + path, data=data,
                                   cookies=cookies, allow_redirects=True)
            time1 = time.time()
            opts['timer_file'].write('%f,%f,%s,%s\n' % (time1-time0, time.time(),
                                                        method, path))
            return ret
        else:
            return requests.request(method, opts['url'] + path + '?format=json', data=data,
                                    cookies=cookies, allow_redirects=True)

    @staticmethod
    def post_reply(opts, cookies, thread, content):
        data = {"content": content}
        return YayAPIClient.time_req(opts, 'post', thread, data, cookies)

    @staticmethod
    def register(opts, username, email, password, confirm_password):
        creds = dict(username = username,
                     email = email,
                     password = password)
        creds["confirm-password"] = confirm_password
        return YayAPIClient.time_req(opts, 'post', 'auth/register', data=creds)

    @staticmethod
    def login(opts, username, password):
        creds = dict(username = username, password = password)
        return YayAPIClient.time_req(opts, 'post', 'auth/login', creds)

    @staticmethod
    def logout(opts, cookies):
        return YayAPIClient.time_req(opts, 'post', 'auth/logout', [], cookies)

    @staticmethod
    def forgot_password_key(opts):
        return YayAPIClient.time_req(opts, 'get', 'auth/forgot_password')

    @staticmethod
    def edit_title(opts, cookies, title):
        data = dict(title = title)
        return YayAPIClient.time_req(opts, 'post', 'title/edit', data, cookies)

    @staticmethod
    def forgot_password(opts, email, key=None):
        cookies=[]

        if (None == key):
            r = YayAPIClient.forgot_password_key(opts)
            cookies = r.cookies
            j = json.loads(r.content)
            key = j['key']

        creds = dict(email = email, key = key)

        return YayAPIClient.time_req(opts, 'post', 'auth/forgot_password', creds, cookies)


    @staticmethod
    def is_logged_in(details, cookies):
        r = requests.get(details['url'] + 'f/discussions', cookies=cookies)
        tree = lxml.html.fromstring(r.content)
        return not not tree.cssselect(".welcome")
