import unittest

from control_tests.control_test1.task2.wc_simple import process_file

PATH_TO_DIR_WITH_FILES = "tests/control_test1/task2/res"


class WcTestCase(unittest.TestCase):
    def test_file_with_many_lines(self):
        stats = process_file(f"{PATH_TO_DIR_WITH_FILES}/many_lines.txt")
        self.assertEqual(stats, (25, 42, 539))

    def test_empty_file(self):
        stats = process_file(f"{PATH_TO_DIR_WITH_FILES}/empty.txt")
        self.assertEqual(stats, (0, 0, 0))

    def test_file_with_emoji(self):
        stats = process_file(f"{PATH_TO_DIR_WITH_FILES}/emoji.txt")
        self.assertEqual(stats, (1, 7, 41))

    def test_blank_file(self):
        stats = process_file(f"{PATH_TO_DIR_WITH_FILES}/blank_file.txt")
        self.assertEqual(stats, (31, 0, 31))
