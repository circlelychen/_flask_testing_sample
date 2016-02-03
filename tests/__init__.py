
# -*- coding: utf-8 -*-
"""
    tests
    ~~~~~

    tests package
"""
import os
import json
import sys
import logging
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

from unittest import TestCase
from flask import Request
from werkzeug.datastructures import MultiDict


from .helper import TestingFileStorage

import application 

class FlaskTestCase(TestCase):

    def _create_fixtures(self):
        pass

    def _drop_fixtures(self):
        pass

    def _detach_logger_format(self):
        self._logger.removeHandler(self._console)
        self.app.logger.removeHandler(self._console)
        pass

    def _attach_logger_format(self, level = logging.CRITICAL):
        self._logger = logging.getLogger(__name__)
        self._console = logging.StreamHandler()
        formatter = logging.Formatter("%(levelname)s "
                                      ": [%(message)s] "
                                      "[in %(filename)s: %(funcName)s: %(lineno)d]")
        self._console.setFormatter(formatter)
        self._logger.addHandler(self._console)
        self._logger.setLevel(level)

        self.app.logger.setLevel(level)

    def setUp(self):
        super(FlaskTestCase, self).setUp()
        self.app = application.create_app("app", "config.TestingConfig")
        self.app_context = self.app.app_context()
        self.app_context.push()

        # !important must init_app after current_app is existed
        from application import init_app
        self.app = init_app(self.app)
        # !important must init_app after current_app is existed

        self.client = self.app.test_client(use_cookies=True)
        self._attach_logger_format(level = logging.DEBUG)

        # DO NOT move "import factories" from here
        import factories
        # DO NOT move "import factories" from here
        self._db = factories.init_db(self.app)
        self._create_fixtures()

    def tearDown(self):
        super(FlaskTestCase, self).tearDown()
        self._drop_fixtures()
        self._db.drop_all()
        self._detach_logger_format()
        self.app_context.pop()

    def _json_data(self, kwargs, csrf_enabled=True):
        if 'data' in kwargs:
            self._logger.info("type of data: {0}".format(type(kwargs["data"])))
            kwargs['data'] = json.dumps(kwargs['data'])
            self._logger.info("data: ## {0} ##".format(kwargs["data"]))
        if not kwargs.get('content_type'):
            kwargs['content_type'] = 'application/json'
        return kwargs

    def _request(self, method, *args, **kwargs):
        kwargs.setdefault('follow_redirects', True)
        return method(*args, **kwargs)

    def _jrequest(self, *args, **kwargs):
        return self._request(*args, **kwargs)

    def post_with_file(self, *args, **kwargs):
        class TestingRequest(Request):
            """A testing request to use that will return a
            TestingFileStorage to test the uploading."""
            @property
            def files(self):
                d = MultiDict()
                d['file'] = TestingFileStorage(
                    stream=kwargs['data']['file'][0],
                    filename=kwargs['data']['file'][1])
                return d
#            def _get_file_stream(*args, **kwargs):
#                return TestingFile()

        self.new_app = self._create_app()
        self.new_app.request_class = TestingRequest
        test_client = self.new_app.test_client(use_cookies=True)
        return self._request(test_client.post, *args, **kwargs)

    def get(self, *args, **kwargs):
        return self._request(self.client.get, *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._request(self.client.delete, *args, **kwargs)

    def jget(self, *args, **kwargs):
        return self._jrequest(self.client.get, *args,
                              **self._json_data(kwargs))

    def post(self, *args, **kwargs):
        return self._request(self.client.post, *args, **kwargs)

    def jpost(self, *args, **kwargs):
        return self._jrequest(self.client.post, *args,
                              **self._json_data(kwargs))

    def put(self, *args, **kwargs):
        return self._request(self.client.put, *args, **kwargs)

    def jput(self, *args, **kwargs):
        return self._jrequest(self.client.put, *args,
                              **self._json_data(kwargs))

    def jdelete(self, *args, **kwargs):
        return self._jrequest(self.client.delete, *args, **kwargs)

    def assertStatusCode(self, response, status_code):
        """Assert the status code of a Flask test client response

        :param response: The test client response object
        :param status_code: The expected status code
        """
        self.assertEquals(status_code, response.status_code)
        return response

    def assertOk(self, response):
        """Test that response status code is 200

        :param response: The test client response object
        """
        return self.assertStatusCode(response, 200)

    def assertBadRequest(self, response):
        """Test that response status code is 400

        :param response: The test client response object
        """
        return self.assertStatusCode(response, 400)

    def assertForbidden(self, response):
        """Test that response status code is 403

        :param response: The test client response object
        """
        return self.assertStatusCode(response, 403)

    def assertNotFound(self, response):
        """Test that response status code is 404

        :param response: The test client response object
        """
        return self.assertStatusCode(response, 404)

    def assertContentType(self, response, content_type):
        """Assert the content-type of a Flask test client response

        :param response: The test client response object
        :param content_type: The expected content type
        """
        self.assertEquals(content_type, response.headers['Content-Type'])
        return response

    def assertJson(self, response):
        """Test that content returned is in JSON format

        :param response: The test client response object
        """
        return self.assertContentType(response, 'application/json')

    def assertHtmlUtf8(self, response):
        """Test that content returned is in JSON format

        :param response: The test client response object
        """
        return self.assertContentType(response, 'text/html; charset=utf-8')

    def assertPlainUtf8(self, response):
        """Test that content returned is in JSON format

        :param response: The test client response object
        """
        return self.assertContentType(response, 'text/plain; charset=utf-8')

    def assertOkJson(self, response):
        """Assert the response status code is 200 and a JSON response

        :param response: The test client response object
        """
        return self.assertOk(self.assertJson(response))

    def assertJsonEqual(self, jresp, expected):
        def check_equal(key, val):
            self.assertEquals(jresp[key], val)
        for key, val in expected.iteritems():
            check_equal(key, val)
        pass

    def assertBadJson(self, response):
        """Assert the response status code is 400 and a JSON response

        :param response: The test client response object
        """
        return self.assertBadRequest(self.assertJson(response))
