import pandas as pd
import re
import numpy as np
import openpyxl

table_dict={}
def parser(test_string,line_number):
    words=test_string.split(" ")
    words.pop(0)
    words.pop(0)
    words.pop(0)
    words.pop(0)

    for i in words :
        kv_pair=i.split('=')
        key=kv_pair[0]
        if len(kv_pair)==2:
            value=kv_pair[1]
        else:
            value="--"
        if key not in table_dict.keys():
            table_dict[key]=[ ]

        while len(table_dict[key]) < line_number :
            table_dict[key].append("--")

        table_dict[key].append(value)

def parse_fortigate(location1,location2):
    with open(location1, 'r') as fo:
        line=fo.readline()
        line=fo.readline()
        line_number=0
        while line:
            pattern = '["](.*?)["]'
            result = re.findall(pattern, line)
            for i in result:
                j = i.replace(" ", "-")
                line = line.replace(i, j)

            parser(line,line_number)
            line_number=line_number+1
            line=fo.readline()

    for i in table_dict.keys() :
        while len(table_dict[i])<line_number :
            table_dict[i].append("--")


    df=pd.DataFrame.from_dict(table_dict)
    print(df)

    if location2 != "NO" :
        df.to_excel(location2)