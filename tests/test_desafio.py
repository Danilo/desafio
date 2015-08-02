import unittest, urllib2

class TestFunctions(unittest.TestCase):
    def test_insert(self):
        url = 'http://127.0.0.1:5000/person/'
        data = 'facebookId=670286562'
        request = urllib2.Request(url, data)
        content = urllib2.urlopen(request)
        for x in content:
            self.assertEqual(x, 'HTTP 201')
        content.close()

if __name__ == '__main__':
    unittest.main()
