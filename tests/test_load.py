__author__ = 'a-burm'

import unittest
import os
import pyperclip
import shutil
import bpcapture
import bpdeploy

SIMPLE_BOOK = '0eJx1kNEKgzAMRX9F+jzBOkc3f2UMqS4bZW0qbZWJ+O9rO8UN9K25N/ckzUhq2UFrBLqq1vpFymQkvHGih0rgHd5eyA7J2mW9cB3XOgY' \
              'AnXACZi9WQ4WdqsF4ifo8cgX+SazTCOmjM8gbIN5otfVRjZETphVh3BBilE7TzRei0Tijl5UC0oonchlzu3Q3tNEQDhSZaeFZ/vwo9El' \
              'eg4wErloJyZ/Zg7HfDfMzLdglZ0fGTjQrpoBbjrQNT+NRtybM+j58+gCa7oFA'


class TestLoad(unittest.TestCase):
    def setUp(self):
        self.root_path = os.path.abspath('temp')
        os.mkdir(self.root_path)

    def tearDown(self):
        shutil.rmtree(self.root_path)

    def test_consistency(self):
        pyperclip.copy(SIMPLE_BOOK)
        bpcapture.capture_from_clip(self.root_path)
        bpdeploy.deploy_to_clip(os.path.join(self.root_path, "sample book"))
        result = pyperclip.paste()
        self.assertEqual(SIMPLE_BOOK, result)


class TestLoadErrors(unittest.TestCase):
    def setUp(self):
        self.root_path = os.path.abspath('temp')
        os.mkdir(self.root_path)

    def tearDown(self):
        shutil.rmtree(self.root_path)

    def test_invalid_json(self):
        bp_path = os.path.join(self.root_path, "test.json")
        with open(bp_path, 'w') as bp_file:
            bp_file.write('{"blueprint: { }')
        with self.assertRaises(bpdeploy.BpDeployException):
            bpdeploy.deploy_to_clip(bp_path)

    def test_invalid_format(self):
        bp_path = os.path.join(self.root_path, "test.json")
        with open(bp_path, 'w') as bp_file:
            bp_file.write('{"nonexistent: { }}')
        with self.assertRaises(bpdeploy.BpDeployException):
            bpdeploy.deploy_to_clip(bp_path)


if __name__ == '__main__':
    unittest.main()
