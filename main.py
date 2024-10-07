import csv
from datetime import datetime, date
from typing import Tuple, Union, List

def fill_spaces(data: list):
    for i in range(2, len(data)):
        prev_temp, prev_util = float(data[i - 1][1]), float(data[i - 1][2])
        if data[i][1] == '':
            data[i][1] = prev_temp
        if data[i][2] == '':
            data[i][2] = prev_util

def count_stats(data: list, param: str) -> Tuple[Union[int, float], Union[int, float], float]:
    min = max = float(data[1][param])
    avg = 0

    for stat in data[1:]:
        value = float(stat[param])
        if min > value:
            min = value
        if max < value:
            max = value

        avg += value
    
    avg /= (len(data) - 1)

    return min, max, avg

def time_sort(data):
    headers = data[0]

    sorted_data = sorted(data[1:], key=lambda x: datetime.strptime(x[3][:19], '%Y-%m-%d %H:%M:%S').timestamp())
    sorted_data.insert(0, headers)

    return sorted_data

def main(file_path: str) -> None:
    with open(file_path, "r", newline='') as file:
        reader = csv.reader(file, delimiter=';')
        data = list(reader)
        fill_spaces(data)
    # добавление новых полей    
    min_temp, max_temp, avg_temp = count_stats(data, 1)
    min_util, max_util, avg_util = count_stats(data, 2)

    new_data = [min_temp, max_temp, avg_temp,
                       min_util, max_util, avg_util] 
    new_headers = ['min_temp', 'max_temp', 'avg_temp',
                   'min_util', 'max_util', 'avg_util', 'status']

    for header in new_headers:
        data[0].append(header)

    for i in range(1, len(data)):
        for stats in new_data:
            data[i].append(stats)
        if (float(data[i][1]) - avg_temp) > 0.3 * max_temp:
            data[i].append('WARNING')
        else:
            data[i].append('OK')
    # добавление новых полей    
    # сортировка по timestamp
    sorted_data = time_sort(data)
    # сортировка по timestamp
    with open(f'logs/{datetime.now()}.csv', "w", newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(sorted_data)


if __name__ == "__main__":
    main("test_data.csv")
