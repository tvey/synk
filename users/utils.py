import csv
import json


def write_txt(qs, stream):
    for item in qs:
        sign = '+' if item.is_done else '-'
        line = f'{sign} {item.text}\n'
        stream.write(line)

    return stream


def write_csv(qs, stream):
    wr = csv.writer(stream)
    wr.writerow(['todo', 'is_done'])

    for item in qs:
        is_done = 1 if item.is_done else 0
        wr.writerow([item.text, is_done])

    return stream


def write_md(qs, stream):
    for item in qs:
        sign = 'x' if item.is_done else ' '
        line = f'- [{sign}] {item.text}\n'
        stream.write(line)

    return stream


def write_json(qs, stream):
    data = []

    for item in qs:
        elem = {'todo': item.text, 'is_done': item.is_done}
        data.append(elem)
    json.dump(data, stream, indent=4)

    return stream
