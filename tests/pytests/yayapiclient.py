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
    def list_threads(opts, pagination_start=None, filter=None):
        path = ''

        if (pagination_start):
            path += 'p/' + str(pagination_start) + '/'

        if (filter):
            path += 'f/' + filter + '/'

        if (pagination_start):
            path += 'desc/'

        # strip trailing /
        path = path.rstrip('/')

        return YayAPIClient.time_req(opts, 'get', path)

    @staticmethod
    def search(opts, term, pagination_start=None):
        path = 'find/' + term

        if (pagination_start):
            path += '/p/' + str(pagination_start) + '/desc'

        return YayAPIClient.time_req(opts, 'get', path)

    @staticmethod
    def post_thread(opts, cookies, cat, subject, content):
        data = {
            "category[]": str(cat),
            "content": content,
            "subject": subject
        }
        return YayAPIClient.time_req(opts, 'post', 'newthread', data, cookies)

    @staticmethod
    def get_thread(opts, thread_id):
        return YayAPIClient.time_req(opts, 'get', 'thread/' + str(thread_id))

    @staticmethod
    def post_comment(opts, cookies, thread_id, content):
        data = {"content": content}
        return YayAPIClient.time_req(opts, 'post', 'thread/' + str(thread_id), data, cookies)

    @staticmethod
    def edit_comment(opts, cookies, comment_id, content):
        data = {
            'comment_id': comment_id,
            'content': content,
        }

        return YayAPIClient.time_req(opts, 'post', 'ajax/comment_save', data, cookies)

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
    def get_inbox(opts, cookies):
        return YayAPIClient.time_req(opts, 'get', 'messages/inbox', [], cookies)

    @staticmethod
    def get_outbox(opts, cookies):
        return YayAPIClient.time_req(opts, 'get', 'messages/outbox', [], cookies)

    @staticmethod
    def send_message(opts, cookies, to, subject, content, save_to_sent=True, read_receipt=False):
        data = dict(recipients = to,
                    subject = subject,
                    content = content,
                    save_sent = 'save' if save_to_sent else 0,
                    read_receipt = 'receipt' if read_receipt else 0)
        return YayAPIClient.time_req(opts, 'post', 'message/send', data, cookies)

    @staticmethod
    def get_message(opts, cookies, message_id):
        return YayAPIClient.time_req(opts, 'get', 'message/' + str(message_id), [], cookies)

    @staticmethod
    def get_user(opts, username):
        return YayAPIClient.time_req(opts, 'get', 'user/' + username)

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
