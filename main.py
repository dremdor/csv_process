import csv
import json

from datetime import datetime
from typing import Tuple, Union, List, Dict


class CsvProcess:
    """Класс для обработки csv файлов."""

    def __init__(self, file_path: str) -> None:
        """Конструктор, считывающий из csv файла."""
        self.data = self.read_csv(file_path)

    def data_to_float(self) -> None:
        """Метод для перевода вещественный значений из строки в float.
        Также проверяет корректность данных."""
        try:
            for line in self.data[1:]:
                if line[1] != "":
                    line[1] = float(line[1])
                if line[2] != "":
                    line[2] = float(line[2])

        except ValueError as e:
            raise ValueError(f"Corrupted data: {e}")

    def fill_spaces(self) -> None:
        """Метод для заполнения недостающих данных
        Внутри себя преобразует считанные данные из строки в float
        Выдает исключение если данные в первой строке отсутствуют
        т.к. мы должны доставлять недостающие данные из предыдущего
        временного промежутка, иначе данные некорректны."""
        self.data_to_float()

        if not self.data[1][1] or not self.data[1][2]:
            raise ValueError("Impossible to fill data")

        for i in range(2, len(self.data)):
            prev_temp, prev_util = self.data[i - 1][1], self.data[i - 1][2]

            if self.data[i][1] == "":
                self.data[i][1] = prev_temp

            if self.data[i][2] == "":
                self.data[i][2] = prev_util

    def count_stats(self, param: int) -> Tuple[float, float, float]:
        """Метод для расчета статистических данных
        принимает необходимый параметр, номер столбца
        возвращает статистические значения для выборки."""
        min_value = max_value = self.data[1][param]
        avg = 0

        for stat in self.data[1:]:
            value = stat[param]

            min_value = min(min_value, value)
            min_value = max(min_value, value)

            avg += value

        avg /= len(self.data) - 1

        return min_value, max_value, avg

    def add_columns(self) -> None:
        """Метод добавляющий данные к каждой строке
        Также рассчитывает статус по условию."""
        min_temp, max_temp, avg_temp = self.count_stats(1)
        min_util, max_util, avg_util = self.count_stats(2)

        stats_headers = [
            "min_temp",
            "max_temp",
            "avg_temp",
            "min_util",
            "max_util",
            "avg_util",
            "status",
        ]

        stats_data = [min_temp, max_temp, avg_temp, min_util, max_util, avg_util]

        headers = self.data[0]

        for header in stats_headers:
            headers.append(header)

        for line in self.data[1:]:
            for stats in stats_data:
                line.append(stats)

            if (line[1] - avg_temp) > 0.3 * max_temp:
                line.append("WARNING")
            else:
                line.append("OK")

    def time_sort(self) -> None:
        """Метод для сортировки по времени с точностью до микросекунд
        Обрабатывается исключение при некорректном задании времени."""
        headers = ["index"] + self.data[0][1:]

        try:
            sorted_data = sorted(
                self.data[1:],
                key=lambda x: datetime.strptime(
                    x[3][:19], "%Y-%m-%d %H:%M:%S"
                ).timestamp(),
            )
        except ValueError as e:
            raise ValueError(f"Invalid timestamp: {e}")

        for i, line in enumerate(sorted_data):
            line[0] = str(i)

        self.data = [headers] + sorted_data

    def read_csv(self, file_path: str) -> List[List[str]]:
        """Метод для чтения из csv файла
        Обрабатывается исключения:
        пустой файл,
        файл без данных,
        отсутствие файла,
        а также другие связанные с кодировкой и т.п.."""
        try:
            with open(file_path, "r", newline="") as file:
                reader = csv.reader(file, delimiter=";")
                data = list(reader)

            if len(data) == 0:
                raise ValueError(f"File {file_path} is empty")
            elif len(data) == 1:
                raise ValueError(f"File {file_path} have no data")

        except FileNotFoundError:
            raise FileNotFoundError(f"File {file_path} not found")
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Unexpected: {e}")

        return data

    def write_csv(self, save_path: str) -> None:
        """Метод записывающий в файл csv, с названием файл - текущее время
        В качестве аргумента принимает путь до директории."""
        with open(
            f'{save_path}/{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.csv',
            "w",
            newline="",
        ) as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerows(self.data)

    def make_json(self) -> List[Dict[str, Union[str, float]]]:
        """Метод формирующий из списка списков, список словарей для json."""
        json_list = []
        headers = self.data[0]

        for line in self.data[1:]:
            line_json = {headers[i]: line[i] for i in range(len(headers))}
            json_list.append(line_json)

        return json_list

    def write_json(self, save_path: str) -> None:
        """Метод записывающий в файл json, с названием файл - текущее время
        В качестве аргумента принимает путь до директории."""
        json_list = self.make_json()
        with open(
            f'{save_path}/{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.json',
            "w",
            newline="",
        ) as file:
            json.dump(json_list, file, indent=4)

    def process(self) -> None:
        """Метод обработки файла в соответствии с заданием,
        Сортировка идет первой по очереди т.к. с ней связана
        корректность приходящих данных."""
        self.time_sort()
        self.fill_spaces()
        self.add_columns()

        self.write_csv("logs/csv")
        self.write_json("logs/json")


def main() -> None:
    data = CsvProcess("tests/test_data.csv")
    data.process()


if __name__ == "__main__":
    main()
