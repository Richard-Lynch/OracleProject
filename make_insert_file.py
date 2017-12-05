#!/usr/local/bin/python3
import sys
from pprint import pprint
from os import listdir
from os.path import isfile, join


def create_table(create_string, filename, headers):
    primary_string = "\tCONSTRAINT pk_{} PRIMARY KEY ({}),\n"
    foreign_string = "\tCONSTRAINT fk_{} FOREIGN KEY ({})\n\tREFERENCES {} ({})"
    on_del_cascade = " ON DELETE CASCADE"
    table_values = ""
    constraint_values = ""
    names = headers[0]
    col_types = headers[1]
    col_sizes = headers[2]
    col_primary = headers[3]
    col_foreign = headers[4]
    fk_table = headers[5]
    fk_col = headers[6]
    fk_cascade = headers[7]
    for col_name, col_type, col_size, col_p, col_f, fk_t, fk_c, fk_cas in zip(
            names, col_types, col_sizes, col_primary, col_foreign, fk_table,
            fk_col, fk_cascade):
        table_value = "\t{} {}{},\n".format(col_name, col_type,
                                            col_size.strip('"'))
        table_values += table_value

        # check for primary key
        if col_p == "PRIMARY":
            print('col_p matches')
            pk_string = primary_string.format(col_name, col_name)
            constraint_values += pk_string
        if col_f == "FOREIGN":
            print('col_f matches')
            fk_string = foreign_string.format(col_name, col_name, fk_t, fk_c)
            if fk_cas == "DEL":
                fk_string += on_del_cascade
            fk_string += ",\n"
            constraint_values += fk_string

    print("--")
    print('table values')
    print(table_values)
    if constraint_values == "":
        table_values = table_values[:-2] + "\n"
    else:
        constraint_values = constraint_values[:-2] + "\n"
        table_values += constraint_values
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
        'date': '\'{}\'',
    }
    header_strings = ', '.join(headers[0])
    insert_values = ""
    for row in data:
        insert_value = []
        for value, col_type in zip(row, headers[1]):
            try:
                if value == "":
                    insert_value.append(type_wrap['Number'].format('null'))
                else:
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


header_lines = 8

create_table_string = 'create table {}(\n{});'
insert_string = 'insert into {}  ({}) values ({});\n'
file_string = '{}\nselect * from {};\ndrop table {}\nquit;\n/'

table_path = '/Users/richie/programs/OracleProject/table_data/'
create_insert_path = '/Users/richie/programs/OracleProject/insert_scripts/'
create_table_path = '/Users/richie/programs/OracleProject/create_scripts/'
both_path = '/Users/richie/programs/OracleProject/both_scripts/'

onlyfiles = [
    f.split('.')[0] for f in listdir(table_path)
    if isfile(join(table_path, f))
]
print(onlyfiles)
created_tables = {}
created_inserts = {}
created_both = {}
for filename in onlyfiles:
    if filename == "":
        continue
    with open(table_path + filename + ".txt") as f:
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

file_string = '{}\nselect * from {};\ndrop table {};\nquit;\n/'
print('---table---')
for k, v in created_tables.items():
    print("{}\n{}".format(k, v))
    fn = create_table_path + k + ".sql"
    with open(fn, "w+") as f:
        f.write(v)
print('---insert---')
for k, v in created_inserts.items():
    print("{}\n{}".format(k, v))
    fn = create_insert_path + k + ".sql"
    with open(fn, "w+") as f:
        f.write(v)
print('---both---')
for k, v in created_both.items():
    print("{}\n{}".format(k, v))
    fn = both_path + k + ".sql"
    with open(fn, "w+") as f:
        f.write(file_string.format(v, k, k))

sys.exit()
