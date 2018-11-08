import json
import unittest
from bson.json_util import dumps
from bson.regex import Regex
from datetime import datetime

from database import setup_db
from main import app


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.collection = setup_db()

    def test_get_call_with_no_queries_succeeds(self):
        response = self.app.get('/bbc')
        self.assertEqual(response.status_code, 200)

    def test_tag_param_works(self):
        query_tag = 'Canada'
        response = self.app.get('/bbc?tag={}'.format(query_tag))
        json_arr = json.loads(response.data)
        for res in json_arr:
            self.assertIn(query_tag, res['tag'])

    def test_title_param_works(self):
        query_title = 'US'
        response = self.app.get('/bbc?title={}'.format(query_title))
        json_arr = json.loads(response.data)
        for res in json_arr:
            self.assertIn(query_title, res['title'])

    def test_api_retrieves_all_the_data(self):
        items = self.collection.find(
            {'scraped_date': datetime.now().strftime("%Y-%m-%d")})
        json_arr = json.loads(self.app.get('/bbc').data)
        self.assertEqual(len(json_arr), len(json.loads(dumps(items))))

if __name__ == '__main__':
    unittest.main()
