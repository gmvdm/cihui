import unittest

from tornado.testing import AsyncHTTPTestCase, LogTrapTestCase
from cihui import app


# class DisplayWordListsTest(AsyncHTTPTestCase, LogTrapTestCase):
class DisplayWordListsTest(AsyncHTTPTestCase):

    def get_app(self):
        return app.CiHuiApplication()

    def setUp(self):
        AsyncHTTPTestCase.setUp(self)

    def test_show_homepage(self):
        self.http_client.fetch(self.get_url('/'), self.stop)
        response = self.wait()

        self.assertEqual(200, response.code)

    def test_invalid_url(self):
        self.http_client.fetch(self.get_url('/fish'), self.stop)
        response = self.wait()

        self.assertEqual(404, response.code)


if __name__ == '__main__':
    unittest.main()
