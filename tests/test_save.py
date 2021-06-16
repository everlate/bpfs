__author__ = 'a-burm'

import unittest
import bpcapture
import pyperclip
import os
import shutil


SIMPLE_BOOK = '0eNp9kF0KgzAQhK9S9jmCsRbbXKUUiXZbQuNGTJSK5O41kaLQn8eZ3f1m2Akq3WPbKXJlZcwDxLQ6FsR5I8NM1YYW26o7SR08N7YIAp' \
              'TDBhiQbIKyzhAmt74jWSN4Boqu+ATB/YUBklNO4QKKYiypbyrs5oUfCAatsfOVoZA5k/KUwTjvc+4DM8aLTVsGWlaoA0g2rcbddjRgZ' \
              'yMqO/K8OGXFvigOPM3Xouk3aBJ/9EleXFk7NWD5BvxJ8S/eCXzA'

NO_NAME_BOOK = '0eNp9kMEOgjAQRP9lzyWhiKn2V4whBVfTCFtCC5GQ/rttiYGDepzZ2beTXaBuR+wHTa6qjXmCXDbHgrzsZJzpxtBqW/0g1UbPzT2CB' \
               'O2wAwakuqisM4TZfRxINQiegaYbvkByf2WA5LTTuIKSmCsauxqHEPiBYNAbG7YMxZuBVOYM5pDn3EdmOi93bRlMONiUL068FOdCHIQ' \
               '48rzc2uTfNrP0CAaqcXrC6hP9w/Nv9UlsIA=='

DUPLICATES = '0eNrlktEOgjAMRf+lzyNhiEH3K8aQAdU0QkfYMBKzf3eDGHhQf8DHe9ed3jZ9QtWO2A/ErqyMuYF6ro4FddrI+Ea14cW2dGXdRs9NPYI' \
             'CctiBANZdVNYZxuQyDqxrBC+AuMEHKOnPApAdOcIFNIup5LGrcAgFXxACemPDL8OxZyDlqYAp1EvpI3NurzZpBbS6wpAQmrFvqdYuQu4' \
             '42JmRHWReHLNiVxR7meZrwtSL/xtafqIl80UI0LWjO5bv/fzg+RdL/sMZ'


class TestSave(unittest.TestCase):
    def setUp(self):
        self.root_path = os.path.abspath('temp')
        os.mkdir(self.root_path)

    def tearDown(self):
        shutil.rmtree(self.root_path)

    def test_simple_book(self):
        pyperclip.copy(SIMPLE_BOOK)
        bpcapture.capture_from_clip(self.root_path)
        book_path = os.path.join(self.root_path, "sample book")
        self.assertTrue(os.path.isdir(book_path), book_path)
        bp_path = os.path.join(book_path, ".book.json")
        self.assertTrue(os.path.isfile(bp_path), str(os.listdir(book_path)))
        bp_path = os.path.join(book_path, "sample blueprint.json")
        self.assertTrue(os.path.isfile(bp_path), str(os.listdir(book_path)))

    def test_no_name(self):
        pyperclip.copy(NO_NAME_BOOK)
        bpcapture.capture_from_clip(self.root_path)
        book_path = os.path.join(self.root_path, "blueprint")
        self.assertTrue(os.path.isdir(book_path), book_path)
        bp_path = os.path.join(book_path, ".book.json")
        self.assertTrue(os.path.isfile(bp_path), str(os.listdir(book_path)))
        bp_path = os.path.join(book_path, "blueprint.json")
        self.assertTrue(os.path.isfile(bp_path), str(os.listdir(book_path)))

    def test_duplicates(self):
        pyperclip.copy(DUPLICATES)
        bpcapture.capture_from_clip(self.root_path)
        book_path = os.path.join(self.root_path, "blueprint")
        self.assertTrue(os.path.isdir(book_path), book_path)
        bp_path = os.path.join(book_path, ".book.json")
        self.assertTrue(os.path.isfile(bp_path), str(os.listdir(book_path)))
        bp_path = os.path.join(book_path, "duplicate.json")
        self.assertTrue(os.path.isfile(bp_path), str(os.listdir(book_path)))
        bp_path0 = os.path.join(book_path, "duplicate.0.json")
        bp_path1 = os.path.join(book_path, "duplicate.1.json")
        self.assertTrue(os.path.isfile(bp_path0) or os.path.isfile(bp_path1), str(os.listdir(book_path)))

    def test_overwrite(self):
        pyperclip.copy(DUPLICATES)
        bpcapture.capture_from_clip(self.root_path)
        pyperclip.copy(NO_NAME_BOOK)
        bpcapture.capture_from_clip(self.root_path)
        book_path = os.path.join(self.root_path, "blueprint")
        self.assertTrue(os.path.isdir(book_path), book_path)
        bp_path = os.path.join(book_path, ".book.json")
        self.assertTrue(os.path.isfile(bp_path), bp_path)
        bp_path = os.path.join(book_path, "blueprint.json")
        self.assertTrue(os.path.isfile(bp_path), bp_path)


class TestSaveErrors(unittest.TestCase):
    def setUp(self):
        self.root_path = os.path.abspath('temp')
        os.mkdir(self.root_path)

    def tearDown(self):
        shutil.rmtree(self.root_path)

    def test_empty(self):
        pyperclip.copy("")
        with self.assertRaises(bpcapture.BpCaptureException):
            bpcapture.capture_from_clip(self.root_path)

    def test_invalid_clip(self):
        pyperclip.copy("012345")
        with self.assertRaises(bpcapture.BpCaptureException):
            bpcapture.capture_from_clip(self.root_path)

    def test_bad_path(self):
        pyperclip.copy(SIMPLE_BOOK)
        with self.assertRaises(bpcapture.BpCaptureException):
            bpcapture.capture_from_clip(os.path.join(self.root_path, "nonexistent"))

    def test_non_json_delete(self):
        pyperclip.copy(SIMPLE_BOOK)
        bpcapture.capture_from_clip(self.root_path)
        book_path = os.path.join(self.root_path, "sample book")
        bp_path = os.path.join(book_path, "not_json_file")
        with open(bp_path, 'w') as non_json:
            non_json.write("I am not json file")
        with self.assertRaises(bpcapture.BpCaptureException):
            bpcapture.capture_from_clip(self.root_path)


if __name__ == '__main__':
    unittest.main()
