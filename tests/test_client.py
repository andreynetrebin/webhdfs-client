import unittest
from webhdfs_client.client import WebHDFSClient

class TestWebHDFSClient(unittest.TestCase):
    def setUp(self):
        self.client = WebHDFSClient('http://localhost:50070/webhdfs/v1', username='hdfs')

    def test_list_status(self):
        status = self.client.list_status('/')
        self.assertIsInstance(status, dict)

    def test_create_and_delete_directory(self):
        self.client.mkdirs('/test_dir')
        status = self.client.get_file_status('/test_dir')
        self.assertIsNotNone(status)
        self.client.delete_file('/test_dir', recursive=True)

if __name__ == '__main__':
    unittest.main()
