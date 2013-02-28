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

    def reset(self):
        DbClient.reset_database(self.cfg.get('db', 'host'),     self.cfg.get('db', 'database'),
                                self.cfg.get('db', 'username'), self.cfg.get('db', 'password'))

    @classmethod
    def setUpClass(cls):
        cfg = SafeConfigParser()
        cfg.read(['../yay.ini', 'tests/yay.ini'])
        cls.opts = dict(
            url = cfg.get('site', 'url')
        )

        cls.cfg = cfg

        DbClient.reset_database(cls.cfg.get('db', 'host'),     cls.cfg.get('db', 'database'),
                                cls.cfg.get('db', 'username'), cls.cfg.get('db', 'password'))

        # user = YayClient.register(cls.opts, 'yayapitester', 'yayapitester@example.com', 'api', 'api')
        # thread = YayClient.post_thread(cls.opts, user.cookies, 2, "Test thread", "Test thread content")

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

    def test_forgot_password(self):
        YayAPIClient.register(self.opts, 'testforgotpassword1', 'testforgotpassword1@example.com', 'a', 'a')

        r = YayAPIClient.forgot_password(self.opts, 'testforgotpassword1@example.com')
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertFalse('error' in j)
        self.assertTrue('ok' in j)

    def test_forgot_password_key(self):
        r = YayAPIClient.forgot_password_key(self.opts)
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertTrue('key' in j)

    def test_forgot_password_fail(self):
        YayAPIClient.register(self.opts, 'testforgotpasswordfail1', 'testforgotpasswordfail1@example.com', 'a', 'a')

        r = YayAPIClient.forgot_password(self.opts, 'nonexistant@example.com')
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 412)
        self.assertTrue('error' in j)

        r = YayAPIClient.forgot_password(self.opts, 'testforgotpasswordfail1@example.com', 'xxx')
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 412)
        self.assertTrue('error' in j)

    def test_logout(self):
        r = YayAPIClient.register(self.opts, 'testlogout1', 'testlogout1@example.com', 'a', 'a')
        self.assertTrue(YayAPIClient.is_logged_in(self.opts, r.cookies))
        r = YayAPIClient.logout(self.opts, r.cookies)
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertFalse('error' in j)
        self.assertTrue('ok' in j)
        self.assertFalse(YayAPIClient.is_logged_in(self.opts, r.cookies))

    def test_edit_title(self):
        r = YayAPIClient.register(self.opts, 'testsettitle1', 'testsettitle1@example.com', 'a', 'a')
        r = YayAPIClient.edit_title(self.opts, r.cookies, "foo")
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertFalse('error' in j)
        self.assertTrue('ok' in j)
        self.assertTrue('title' in j)

    def test_edit_title_fail(self):
        r = YayAPIClient.register(self.opts, 'testsettitle1', 'testsettitle1@example.com', 'a', 'a')
        r = YayAPIClient.edit_title(self.opts, r.cookies, "")
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 412)
        self.assertTrue('error' in j)

    def test_create_thread(self):
        r = YayAPIClient.register(self.opts, 'testcreatethread1', 'testcreatethread1@example.com', 'a', 'a')

        for i in xrange(1, 5):
            r = YayAPIClient.post_thread(self.opts, r.cookies, i, 'testcreatethread1 ' + str(i), 'testcreatethread1 ' + str(i) + ' body')
            j = json.loads(r.content)
            self.assertEqual(r.status_code, 201)
            self.assertTrue('thread_id' in j)

    def test_view_thread(self):
        r = YayAPIClient.register(self.opts, 'testviewthread1', 'testviewthread1@example.com', 'a', 'a')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 1, 'testviewthread1 1', 'testviewthread1 1 body')
        j = json.loads(r.content)
        r = YayAPIClient.get_thread(self.opts, j['thread_id'])
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertTrue('comments' in j)
        self.assertEqual(j['pagination']['row_count'], 1)


    def test_create_comment(self):
        r = YayAPIClient.register(self.opts, 'testcreatecomment1', 'testcreatecomment1@example.com', 'a', 'a')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 1, 'testcreatecomment1 1', 'testcreatecomment1 1 body')
        j = json.loads(r.content)
        r = YayAPIClient.post_comment(self.opts, r.cookies, j['thread_id'], 'testcreatecomment1 1 reply')
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 201)
        self.assertTrue('comment_id' in j)
        self.assertTrue('thread_id' in j)
        r = YayAPIClient.get_thread(self.opts, j['thread_id'])
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertTrue('comments' in j)
        self.assertEqual(j['pagination']['row_count'], 2)

    def test_edit_comment(self):
        r = YayAPIClient.register(self.opts, 'testeditcomment1', 'testeditcomment1@example.com', 'a', 'a')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 1, 'testeditcomment1 1', 'testeditcomment1 1 body')
        j = json.loads(r.content)
        r = YayAPIClient.post_comment(self.opts, r.cookies, j['thread_id'], 'testeditcomment1 1 reply')
        j = json.loads(r.content)
        r = YayAPIClient.edit_comment(self.opts, r.cookies, j['comment_id'], 'testeditcomment1 1 reply edit')
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 201)
        self.assertTrue('comment_id' in j)
        self.assertTrue('thread_id' in j)

    def test_list_threads(self):
        self.reset()
        r = YayAPIClient.register(self.opts, 'testlistthreads1', 'testlistthreads1@example.com', 'a', 'a')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 1, 'testlistthreads1 1', 'testlistthreads1 1 body')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 1, 'testlistthreads1 2', 'testlistthreads1 2 body')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 1, 'testlistthreads1 3', 'testlistthreads1 3 body')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 1, 'testlistthreads1 4', 'testlistthreads1 4 body')
        r = YayAPIClient.list_threads(self.opts)
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertTrue('threads' in j)
        self.assertEqual(j['pagination']['row_count'], 4)

    @unittest.skip("pagination is kind of a dick")
    def test_paginate_threads(self):
        self.reset()
        r = YayAPIClient.register(self.opts, 'testpaginatethreads1', 'testpaginatethreads1@example.com', 'a', 'a')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 1, 'testpaginatethreads1 1', 'testpaginatethreads1 1 body')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 2, 'testpaginatethreads1 2', 'testpaginatethreads1 2 body')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 3, 'testpaginatethreads1 3', 'testpaginatethreads1 3 body')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 4, 'testpaginatethreads1 4', 'testpaginatethreads1 4 body')
        r = YayAPIClient.list_threads(self.opts, 100)
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertTrue('threads' in j)
        self.assertEqual(j['pagination']['current_page'], 2)

    def test_list_threads_in_category(self):
        self.reset()
        r = YayAPIClient.register(self.opts, 'testlistthreadsincategory1', 'testlistthreadsincategory1@example.com', 'a', 'a')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 1, 'testlistthreadsincategory1 1', 'testlistthreadsincategory1 1 body')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 2, 'testlistthreadsincategory1 2', 'testlistthreadsincategory1 2 body')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 3, 'testlistthreadsincategory1 3', 'testlistthreadsincategory1 3 body')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 4, 'testlistthreadsincategory1 4', 'testlistthreadsincategory1 4 body')
        r = YayAPIClient.list_threads(self.opts, None, 'discussions')
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertTrue('threads' in j)
        self.assertEqual(j['pagination']['row_count'], 1)

    def test_list_threads_in_search(self):
        self.reset()
        r = YayAPIClient.register(self.opts, 'testlistthreadsinsearch1', 'testlistthreadsinsearch1@example.com', 'a', 'a')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 1, 'testlistthreadsinsearch1 1', 'testlistthreadsinsearch1 1 body')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 2, 'teXstlistthreadsinsearch1 2', 'testlistthreadsinsearch1 2 body')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 3, 'testlistthreadsinsearch1 3', 'testlistthreadsinsearch1 3 body')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 4, 'teXstlistthreadsinsearch1 4', 'testlistthreadsinsearch1 4 body')
        r = YayAPIClient.search(self.opts, 'teXst')
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertTrue('threads' in j)
        self.assertEqual(j['pagination']['row_count'], 2)

    @unittest.skip("pagination is kind of a dick")
    def test_paginate_threads_in_search(self):
        self.reset()
        r = YayAPIClient.register(self.opts, 'testpaginatethreadsinsearch1', 'testpaginatethreadsinsearch1@example.com', 'a', 'a')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 1, 'testpaginatethreadsinsearch1 1', 'testpaginatethreadsinsearch1 1 body')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 2, 'testpaginatethreadsinsearch1 2', 'testpaginatethreadsinsearch1 2 body')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 3, 'testpaginatethreadsinsearch1 3', 'testpaginatethreadsinsearch1 3 body')
        r = YayAPIClient.post_thread(self.opts, r.cookies, 4, 'testpaginatethreadsinsearch1 4', 'testpaginatethreadsinsearch1 4 body')
        r = YayAPIClient.search(self.opts, 'foo', 100)
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertTrue('threads' in j)
        self.assertEqual(j['pagination']['current_page'], 2)

    @unittest.skip("skipping not implemented test")
    def test_paginate_thread(self):
        self.fail("not implemented")

    def test_list_messages_inbox(self):
        self.reset()
        u1 = YayAPIClient.register(self.opts, 'testlistmessagesinbox1', 'testlistmessagesinbox1@example.com', 'a', 'a')
        u2 = YayAPIClient.register(self.opts, 'testlistmessagesinbox2', 'testlistmessagesinbox2@example.com', 'a', 'a')
        r = YayAPIClient.get_inbox(self.opts, u1.cookies)
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertTrue('messages' in j)
        self.assertEqual(len(j['messages']), 0)
        r = YayAPIClient.send_message(self.opts, u2.cookies, 'testlistmessagesinbox1', 'subject', 'body')
        r = YayAPIClient.get_inbox(self.opts, u1.cookies)
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertTrue('messages' in j)
        self.assertEqual(len(j['messages']), 1)

    def test_list_messages_outbox(self):
        self.reset()
        u1 = YayAPIClient.register(self.opts, 'testlistmessagesoutbox1', 'testlistmessagesoutbox1@example.com', 'a', 'a')
        u2 = YayAPIClient.register(self.opts, 'testlistmessagesoutbox2', 'testlistmessagesoutbox2@example.com', 'a', 'a')
        r = YayAPIClient.send_message(self.opts, u2.cookies, 'testlistmessagesoutbox1', 'subject', 'body')
        r = YayAPIClient.get_outbox(self.opts, u2.cookies)
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertTrue('messages' in j)
        self.assertEqual(len(j['messages']), 1)

    def test_create_message(self):
        self.reset()
        u1 = YayAPIClient.register(self.opts, 'testcreatemessage1', 'testcreatemessage1@example.com', 'a', 'a')
        u2 = YayAPIClient.register(self.opts, 'testcreatemessage2', 'testcreatemessage2@example.com', 'a', 'a')
        r = YayAPIClient.get_inbox(self.opts, u1.cookies)
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertTrue('messages' in j)
        self.assertEqual(len(j['messages']), 0)
        r = YayAPIClient.send_message(self.opts, u2.cookies, 'testcreatemessage1', 'subject', 'body')
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 201)
        self.assertTrue('message_id' in j)

    def test_read_message(self):
        self.reset()
        u1 = YayAPIClient.register(self.opts, 'testreadmessage1', 'testreadmessage1@example.com', 'a', 'a')
        u2 = YayAPIClient.register(self.opts, 'testreadmessage2', 'testreadmessage2@example.com', 'a', 'a')
        r = YayAPIClient.get_inbox(self.opts, u1.cookies)
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertTrue('messages' in j)
        self.assertEqual(len(j['messages']), 0)
        r = YayAPIClient.send_message(self.opts, u2.cookies, 'testreadmessage1', 'subject', 'body')
        j = json.loads(r.content)
        r = YayAPIClient.get_message(self.opts, u1.cookies, j['message_id'])
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertTrue('message' in j)
        self.assertTrue('subject' in j['message'])
        self.assertTrue('content' in j['message'])

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

    def test_view_user(self):
        u = YayAPIClient.register(self.opts, 'testviewuser1', 'testviewuser1@example.com', 'a', 'a')
        r = YayAPIClient.get_user(self.opts, 'testviewuser1')
        j = json.loads(r.content)
        self.assertEqual(r.status_code, 200)
        self.assertTrue('id' in j)
        self.assertEqual('testviewuser1', j['username'])

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