import unittest
import my_twitter


class TestMyTwitter(unittest.TestCase):

    def test_generate_twitter_api(self):
        self.assertIsNotNone(my_twitter.generate_twitter_api())

    def test_search_twitter(self):
        my_twitter.search_twitter()


if __name__ == '__main__':
    unittest.main()
