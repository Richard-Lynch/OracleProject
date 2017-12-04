#!/usr/local/bin/python3
import sys
from pprint import pprint
from os import listdir
from os.path import isfile, join


def create_table(create_string, filename, headers):
    table_values = ""
    for name, col_type, size in zip(headers[0], headers[1], headers[2]):
        table_value = "\t{} {}{},\n".format(name, col_type, size.strip('"'))
        table_values += table_value
    print("--")
    print('table values')
    print(table_values)
    result = create_string.format(filename, table_values)
    print("--")
    print('result')
    print(result)
    return result


def create_inserts(insert_string, filename, headers, data):
    type_wrap = {
        'Number': '{}',
        'varchar': '\'{}\'',
        'date': '{}',
    }
    header_strings = ', '.join(headers[0])
    insert_values = ""
    for row in data:
        insert_value = []
        for value, col_type in zip(row, headers[1]):
            try:
                insert_value.append(type_wrap[col_type].format(value))
            except Exception as e:
                print('error', e)
        insert_value = ', '.join(insert_value)
        insert_value = insert_string.format(filename, header_strings,
                                            insert_value)
        insert_values += insert_value
    print("--")
    print('inserted values')
    print(insert_values)
    return insert_values


header_lines = 3

create_table_string = 'create table {}(\n{})'
insert_string = 'insert into {}  ({}) values ({});\n'

mypath = '/Users/richie/programs/OracleProject/table_data/'
onlyfiles = [
    f.split('.')[0] for f in listdir(mypath) if isfile(join(mypath, f))
]
print(onlyfiles)
created_tables = {}
created_inserts = {}
created_both = {}
for filename in onlyfiles:
    with open(mypath + filename + ".txt") as f:
        lis = [line.rstrip('\n').split('\t') for line in f]

    headers = lis[0:header_lines]
    data = lis[header_lines:]

    print(headers[1][0])

    print("--")
    for l in headers:
        print(l)
    print("--")
    for l in data:
        print(l)

    t = create_table(create_table_string, filename, headers)
    i = create_inserts(insert_string, filename, headers, data)
    created_tables[filename] = t
    created_inserts[filename] = i
    created_both[filename] = t + "\n\n" + i

print('---table---')
for k, v in created_tables.items():
    print("{}\n{}".format(k, v))
print('---insert---')
for k, v in created_inserts.items():
    print("{}\n{}".format(k, v))
print('---both---')
for k, v in created_both.items():
    print("{}\n{}".format(k, v))

sys.exit()
