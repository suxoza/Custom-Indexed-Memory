import unittest, json, time
import xml.etree.ElementTree as ET
from main import app

class AppTestCase(unittest.TestCase):

    title = "sfomffddddfe"
    author = "some-audddthor"
    store_id = None

    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

        self.store()

    def tearDown(self):
        self.ctx.pop()

    def store(self):
        response = self.client.post("/submit", data=json.dumps({
            "title": self.title,
            "author": self.author,
            "text": "some-text",
            "url": "http://some-test.com"
        }), content_type = 'application/json')

        assert response.status_code == 201
        self.store_id = response.get_json()['id']

    def search(self, query_path = 'search'):
        response = self.client.get(f'/{query_path}?title=ff')
        assert response.status_code == 200
        return response
        
    def test_get_item(self):
        response = self.client.get(f'/item/{self.store_id}')
        assert response.status_code == 200 and response.get_json()['id'] == self.store_id

    def test_search(self):
        data = self.search().get_json()
        assert len(data) > 0 and data[0]['id'] == self.store_id

    def test_rss(self):
        data = self.search(query_path='rss').get_data().decode()
        tree = ET.fromstring(data)
        channel = tree.find('channel')
        for item in channel.findall('item'):
            assert item.find('title').text == self.title
        
if __name__ == "__main__":
    unittest.main()