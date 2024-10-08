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


class TestCorrectData1(unittest.TestCase):
    def test_correct_data1(self):
        data = CsvProcess("tests/correct1.csv")
        data.time_sort()

        data.fill_spaces()
        data.add_columns()

        ans = [
            [
                "index",
                "temperature",
                "utilization",
                "timestamp",
                "min_temp",
                "max_temp",
                "avg_temp",
                "min_util",
                "max_util",
                "avg_util",
                "status",
            ],
            [
                "0",
                "59.64",
                "37.0",
                "2024-09-27 07:08:32.306912899",
                "59.18",
                "59.64",
                "59.333333333333336",
                "23.0",
                "37.0",
                "27.666666666666668",
                "OK",
            ],
            [
                "1",
                "59.18",
                "23.0",
                "2024-09-27 07:08:37.306912899",
                "59.18",
                "59.64",
                "59.333333333333336",
                "23.0",
                "37.0",
                "27.666666666666668",
                "OK",
            ],
            [
                "2",
                "59.18",
                "23.0",
                "2024-09-27 07:08:42.306912899",
                "59.18",
                "59.64",
                "59.333333333333336",
                "23.0",
                "37.0",
                "27.666666666666668",
                "OK",
            ],
        ]
        self.assertEqual(data.data, ans)


class TestCorrectData2(unittest.TestCase):
    def test_correct_data2(self):
        data = CsvProcess("tests/correct2.csv")
        data.time_sort()

        data.fill_spaces()
        data.add_columns()

        ans = [
            [
                "index",
                "temperature",
                "utilization",
                "timestamp",
                "min_temp",
                "max_temp",
                "avg_temp",
                "min_util",
                "max_util",
                "avg_util",
                "status",
            ],
            [
                "0",
                "59.64",
                "37.0",
                "2024-09-27 07:08:32.306912899",
                "59.18",
                "59.64",
                "59.333333333333336",
                "23.0",
                "37.0",
                "27.666666666666668",
                "OK",
            ],
            [
                "1",
                "59.18",
                "23.0",
                "2024-09-27 07:08:37.306912899",
                "59.18",
                "59.64",
                "59.333333333333336",
                "23.0",
                "37.0",
                "27.666666666666668",
                "OK",
            ],
            [
                "2",
                "59.18",
                "23.0",
                "2024-09-27 07:08:42.306912899",
                "59.18",
                "59.64",
                "59.333333333333336",
                "23.0",
                "37.0",
                "27.666666666666668",
                "OK",
            ],
        ]
        self.assertEqual(data.data, ans)


class TestCorrectData3(unittest.TestCase):
    def test_correct_data3(self):
        data = CsvProcess("tests/correct3.csv")
        data.time_sort()

        data.fill_spaces()
        data.add_columns()

        ans = [
            [
                "index",
                "temperature",
                "utilization",
                "timestamp",
                "min_temp",
                "max_temp",
                "avg_temp",
                "min_util",
                "max_util",
                "avg_util",
                "status",
            ],
            [
                "0",
                "59.64",
                "37.0",
                "2024-09-27 07:08:32.306912899",
                "59.18",
                "59.64",
                "59.333333333333336",
                "23.0",
                "37.0",
                "27.666666666666668",
                "OK",
            ],
            [
                "1",
                "59.18",
                "23.0",
                "2024-09-27 07:08:37.306912899",
                "59.18",
                "59.64",
                "59.333333333333336",
                "23.0",
                "37.0",
                "27.666666666666668",
                "OK",
            ],
            [
                "2",
                "59.18",
                "23.0",
                "2024-09-27 07:08:42.306912899",
                "59.18",
                "59.64",
                "59.333333333333336",
                "23.0",
                "37.0",
                "27.666666666666668",
                "OK",
            ],
        ]
        self.assertEqual(data.data, ans)


if __name__ == "__main__":
    unittest.main()
