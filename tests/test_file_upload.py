import unittest
import json
import sure

from StringIO import StringIO
from . import FlaskTestCase

class FileUploadTestCase(FlaskTestCase): 

    def setUp(self):
        super(FileUploadTestCase, self).setUp()

        self._filename = "example"

    def _create_fixtures(self):
        super(FileUploadTestCase, self)._create_fixtures()
        import factories
        self._file_infos = factories.FileInfoFactory.create_batch(100)
        self._db.session.commit()

    def _drop_fixtures(self):
        super(FileUploadTestCase, self)._drop_fixtures()
        import factories
        factories.FileInfoFactory.reset_sequence(1)

    def test_list_files(self):
        resp = self.get("/files")
        self.assertOk(resp)

        jresp = json.loads(resp.data)
        jresp.get("code", "").must.be.equal(200)
        jresp.get("status", "").must.be.equal("SUCCESS")
        jresp.get("result").must.be.a(list)
        results = jresp.get("result")
        len(results).must.be.equal(len(self._file_infos))

    def test_upload_with_invalid_too_large_file(self):
        resp = self.post("/file", data={
            'file': (StringIO("content "*8*1024*1024), "{0}.{1}".format(self._filename, "txt"))
            })
        self.assertStatusCode(resp, 413)


    def test_upload_file_with_duplicated_filename(self):
        resp = self.post("/file", data={
            'file': (StringIO('my file contents'), self._file_infos[0].file_name)
            })
        self.assertStatusCode(resp, 403)

    @unittest.skip("test_upload_with_invalid_filename_extention")
    def test_upload_with_invalid_filename_extention(self):
        for extension in ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']:
            resp = self.post("/file", data={
                'file': (StringIO("content "), "{0}.{1}".format(self._filename, extension))
                })
            self.assertOk(resp)

        resp = self.post("/file", data={
            'file': (StringIO("content "), "{0}.{1}".format(self._filename, "asdfadsfasd"))
            })
        self.assertBadRequest(resp)

    @unittest.skip("test_upload_file")
    def test_upload_file(self):
        resp = self.post("/file", data={
            'file': (StringIO('my file contents'), 'hello world.txt')
            })
        self._logger.info(resp)
        jresp = json.loads(resp.data)
        jresp.get("code", "").must.be.equal(200)
        jresp.get("status", "").must.be.equal("SUCCESS")
        jresp.get("result").must.be.a(dict)
        result = jresp.get("result")
        result.get("filename").must.be.a(unicode)

