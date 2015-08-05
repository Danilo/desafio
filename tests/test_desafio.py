from flaskext.mysql import MySQL
import unittest, desafio, os, tempfile

desafio.app.config['MYSQL_DATABASE_USER'] = 'root'
desafio.app.config['MYSQL_DATABASE_DB'] = 'testDB'
desafio.app.config['MYSQL_DATABASE_HOST'] = 'localhost'

class DesafioTestCase(unittest.TestCase):
    def setUp(self):
        desafio.app.testing = True
        self.app = desafio.app.test_client()

    def test_delete(self):
        delete = self.app.delete('/person/1447151038885238/')
        assert "HTTP 204" in delete.data

    def test_insert(self):
        data = "1447151038885238"
        post = self.app.post('/person/', data=data)
        assert "HTTP 201" in post.data

    def test_insert_duplicated(self):
        data = "1447151038885238"
        post = self.app.post('/person/', data=data)
        assert "MySQL Error: (1062, \"Duplicate entry \'1447151038885238\' for key \'PRIMARY\'\")" in post.data

    def test_list(self):
        get = self.app.get('/person/?limit=1')
        assert "HTTP 200"
        "["
        "  ["
        "    1447151038885238,"
        "    \"Renato\","
        "    \"Pedigoni\","
        "    \"Renato Pedigoni\""
        "  ]"
        "]" in get.data

if __name__ == '__main__':
    unittest.main()
