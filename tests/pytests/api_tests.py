import unittest
import requests
import simplejson
import lxml
import DbClient
# import simplejson as json
import json

from lxml import html
from urlparse import urlparse
from yayapiclient import YayAPIClient
from ConfigParser import SafeConfigParser

class TestAPIFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cfg = SafeConfigParser()
        cfg.read(['../yay.ini', 'tests/yay.ini'])
        cls.opts = dict(
            url = cfg.get('site', 'url')
        )

        DbClient.reset_database(cfg.get('db', 'host'), cfg.get('db', 'database'),
                                cfg.get('db', 'username'), cfg.get('db', 'password'))

        # user = YayClient.register(cls.opts, 'yay_api_tester', 'api@api.com', 'api', 'api')
        # thread = YayClient.post_thread(cls.opts, user.cookies, 2, "Test", "Test")

        # cls.cookies = user.cookies
        # cls.thread = urlparse(thread.url).path[1:]

    def test_register(self):
        r = YayAPIClient.register(self.opts, 'testregister1', 'test_register1@example.com', 'a', 'a')
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertFalse('errors' in j)
        self.assertTrue('ok' in j)
        self.assertTrue('user_id' in j)
        self.assertEqual(j['username'], 'testregister1')

    def test_register_fail(self):
        r = YayAPIClient.register(self.opts, '    ', 'b@a.com', 'a', 'a')
        j = json.loads(r.content)
        self.assertTrue('errors' in j)
        self.assertTrue('username' in j['errors'])

        r = YayAPIClient.register(self.opts, 'my\'name', 'c@a.com', 'a', 'a')
        j = json.loads(r.content)
        self.assertTrue('errors' in j)
        self.assertTrue('username' in j['errors'])

        r = YayAPIClient.register(self.opts, 'a  b', 'd@a.com', 'a', 'a')
        j = json.loads(r.content)
        self.assertTrue('errors' in j)
        self.assertTrue('username' in j['errors'])

        r = YayAPIClient.register(self.opts, 'a_b', 'e@a.com', 'a', 'a')
        j = json.loads(r.content)
        self.assertTrue('errors' in j)
        self.assertTrue('username' in j['errors'])

        r = YayAPIClient.register(self.opts, 'a-b', 'f@a.com', 'a', 'a')
        j = json.loads(r.content)
        self.assertTrue('errors' in j)
        self.assertTrue('username' in j['errors'])

        r = YayAPIClient.register(self.opts, 'abb', 'facom', 'a', 'a')
        j = json.loads(r.content)
        self.assertTrue('errors' in j)
        self.assertTrue('email' in j['errors'])

        r = YayAPIClient.register(self.opts, 'abc', 'f@a.com', 'a', 'b')
        j = json.loads(r.content)
        self.assertTrue('errors' in j)
        self.assertTrue('confirm-password' in j['errors'])

    def test_login(self):
        YayAPIClient.register(self.opts, 'testlogin1', 'testlogin1@example.com', 'a', 'a')
        r = YayAPIClient.login(self.opts, 'testlogin1', 'a')
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertFalse('error' in j)
        self.assertTrue('ok' in j)
        self.assertTrue('user_id' in j)
        self.assertEqual(j['username'], 'testlogin1')

    def test_login_fail(self):
        r = YayAPIClient.login(self.opts, 'madeupname', 'madeuppass')
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 401)
        self.assertTrue('error' in j)

    @unittest.skip("skipping not implemented test")
    def test_forgot_password(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_forgot_password_fail(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_logout(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_set_title(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_set_title_fail(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_list_threads(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_paginate_threads(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_list_threads_in_category(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_list_threads_in_search(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_paginate_threads_in_search(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_create_thread(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_view_thread(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_paginate_thread(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_create_post(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_edit_post(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_list_messages_inbox(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_paginate_messages_inbox(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_list_messages_outbox(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_paginate_messages_outbox(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_read_message(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_create_message(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_reply_to_message(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_action_message_mark_read(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_action_message_mark_unread(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_action_message_delete_from_inbox(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_action_message_delete_from_outbox(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_list_users(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_paginate_users(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_view_user(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_view_user_fail(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_list_users_buddies(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_paginate_users_buddies(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_add_buddy(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_add_buddy_fail_already_buddy(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_add_buddy_fail_buddy_self(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_move_buddy_to_enemy(self):
        self.fail("not implemented")

    @unittest.skip("skipping not implemented test")
    def test_remove_buddy(self):
        self.fail("not implemented")

    # ajax methods: favourites, new posts, etc
    # preferences

if __name__ == '__main__':
    unittest.main()