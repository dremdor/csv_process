import csv
import json
from datetime import datetime, date
from typing import Tuple, Union, List


def fill_spaces(data: List[List[str]]) -> None:
    for i in range(2, len(data)):
        prev_temp, prev_util = float(data[i - 1][1]), float(data[i - 1][2])

        if data[i][1] == "":
            data[i][1] = prev_temp

        if data[i][2] == "":
            data[i][2] = prev_util


def count_stats(data: List[List[str]], param: int) -> Tuple[float, float, float]:
    min_value = max_value = float(data[1][param])
    avg = 0

    for stat in data[1:]:
        value = float(stat[param])
        if min_value > value:
            min_value = value
        if max_value < value:
            max_value = value

        avg += value

    avg /= len(data) - 1

    return min_value, max_value, avg


def add_columns(data: List[List[str]]) -> None:
    min_temp, max_temp, avg_temp = count_stats(data, 1)
    min_util, max_util, avg_util = count_stats(data, 2)

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

    headers = data[0]

    for header in stats_headers:
        headers.append(header)

    for line in data[1:]:
        for stats in stats_data:
            line.append(stats)

        if (float(line[1]) - avg_temp) > 0.3 * max_temp:
            line.append("WARNING")
        else:
            line.append("OK")


def time_sort(data: List[List[str]]) -> None:
    headers = ["index"] + data[0][1:]

    data[1:].sort(
        key=lambda x: datetime.strptime(x[3][:19], "%Y-%m-%d %H:%M:%S").timestamp(),
    )

    for i, line in enumerate(data):
        line[0] = str(i)

    data[0] = headers


def read_csv(file_path: str) -> List[List[str]]:
    with open(file_path, "r", newline="") as file:
        reader = csv.reader(file, delimiter=";")
        data = list(reader)

    return data


def write_csv(data: List[List[str]]) -> None:
    with open(
        f'logs/csv/{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.csv', "w", newline=""
    ) as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(data)


def write_json(data: List[List[str]]) -> None:
    headers = data[0]
    json_list = []

    for line in data[1:]:
        line_json = {headers[i]: line[i] for i in range(len(headers))}
        json_list.append(line_json)

    with open(
        f'logs/json/{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.csv', "w", newline=""
    ) as file:
        json.dump(json_list, file, indent=4)


def main(file_path: str) -> None:
    data = read_csv(file_path)
    time_sort(data)

    fill_spaces(data)
    add_columns(data)

    write_csv(data)
    write_json(data)


if __name__ == "__main__":
    main("test_data.csv")
    # main('zero.csv')
    # main('headers.csv')
    # main('first_blank.csv')

    # data1 = [
    #    ['temperature', 'utilization', 'timestamp']
    #    ['0', '59.64', '37.0', '2024-09-27 07:08:32.306912899']
    #    ['1', '59.18', '23.0', '2024-09-27 07:08:37.306912899']
    #    ['2', '', '', '2024-09-27 07:08:42.306912899']
    # ]
