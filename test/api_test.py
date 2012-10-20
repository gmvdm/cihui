
import unittest
import urllib

from tornado.testing import AsyncHTTPTestCase
from cihui import app

def build_data(data):
    return urllib.urlencode(data)

class APITest(AsyncHTTPTestCase):


    def get_app(self):
        return app.CiHuiApplication()

    def setUp(self):
        AsyncHTTPTestCase.setUp(self)


    def test_post_new_list(self):
        data = build_data({'email': 'test@example.com',
                           'list': 'Test List',
                           'words': '...'})

        self.http_client.fetch(self.get_url('/api/word'), self.stop, method='POST',
                               headers=None, body=data)
        response = self.wait()

        self.assertEqual(200, response.code)
        self.assertIn('test@example.com', response.body)
