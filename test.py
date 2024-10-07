import unittest
from main import CsvProcess


class TestFileNotFound(unittest.TestCase):
    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError) as error:
            data = CsvProcess("no_file.csv")
        self.assertEqual(str(error.exception), "File no_file.csv not found")


class TestEmptyFile(unittest.TestCase):
    def test_empty_file(self):
        with self.assertRaises(ValueError) as error:
            data = CsvProcess("tests/blank.csv")
        self.assertEqual(str(error.exception), "File tests/blank.csv is empty")


class TestEmptyData(unittest.TestCase):
    def test_empty_data(self):
        with self.assertRaises(ValueError) as error:
            data = CsvProcess("tests/empty.csv")
        self.assertEqual(str(error.exception), "File tests/empty.csv have no data")


class TestEmptyFirstData(unittest.TestCase):
    def test_empty_first_data(self):
        with self.assertRaises(ValueError) as error:
            data = CsvProcess("tests/first_blank.csv")
            data.time_sort()
            data.fill_spaces()
        self.assertEqual(str(error.exception), "Impossible to fill data")


class TestEmptyFullData(unittest.TestCase):
    def test_empty_full_data(self):
        with self.assertRaises(ValueError) as error:
            data = CsvProcess("tests/no_data.csv")
            data.time_sort()
            data.fill_spaces()
        self.assertEqual(str(error.exception), "Impossible to fill data")

    # data1 = [
    #    ['temperature', 'utilization', 'timestamp']
    #    ['0', '59.64', '37.0', '2024-09-27 07:08:32.306912899']
    #    ['1', '59.18', '23.0', '2024-09-27 07:08:37.306912899']
    #    ['2', '', '', '2024-09-27 07:08:42.306912899']
    # ]


if __name__ == "__main__":
    unittest.main()
