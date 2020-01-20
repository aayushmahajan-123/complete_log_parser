import pandas as pd
import re
import numpy as np
import openpyxl

table_rows=[]
def parser(test_string):
    date_pattern = "(?:20[0-9][0-9])\-(?:0[1-9]|1[0-2])\-(?:0[1-9]|1[0-9]|2[0-9]|3[0-1])"
    time_pattern = "T(?:0[0-9]|1[0-9]|2[0-3])\:(?:[0-5][0-9])\:(?:[0-5][0-9])"
    timezone_pattern = "[\+\-](?:0[0-9]|1[0-3])\:(?:00|30|45)"
    ASAincident_pattern="(?:\%[A-Za-z]+)\-(?:[0-9])\-(?:[0-9]+)\:"
    seq_prototype_pattern="(?:[a-zA-Z]+)\s(?:[a-zA-Z]+)\s(?:[a-zA-Z]+)\s(?:[a-zA-Z]+)\s(?:[0-9]+)"
    ip1_pattern="(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\s"
    ip2_pattern="\:(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])/\d+"
    for_pattern="for\s[A-Za-z_0-9]+"
    to_pattern="to\s[A-Za-z_0-9]+"
    new_row=[]
    date = re.findall(date_pattern, test_string)
    new_row.append(date[0])
    time = re.findall(time_pattern, test_string)
    if time:
        xtime = time[0]
        xtime = xtime[1:]
        new_row.append(xtime)
    timezone = re.findall(timezone_pattern, test_string)
    if timezone:
        new_row.append(timezone[0])
    ASA_incident=re.findall(ASAincident_pattern,test_string)
    if ASA_incident :
        new_row.append(ASA_incident[0])
    seq_prototype=re.findall(seq_prototype_pattern,test_string)
    if seq_prototype :
        new_row.append(seq_prototype[0])
    ip1=re.findall(ip1_pattern,test_string)
    if ip1:
        new_row.append(ip1[0])
    for1=re.findall(for_pattern,test_string)
    if for1:
        f=for1[0]
        f=f.split(" ")
        new_row.append(f[1])
    ip2=re.findall(ip2_pattern,test_string)
    if ip2:
        st=ip2[0][1:]
        new_row.append(st)
    to1=re.findall(to_pattern,test_string)
    if to1:
        t=to1[0]
        t=t.split(" ")
        new_row.append(t[1])
    if ip2[1]:
        st=ip2[1][1:]
        new_row.append(st)
    table_rows.append(new_row)


def parse_cisco(location1,location2):
    with open(location1,'r') as fo:
        line=fo.readline()
        while line:
            parser(line)
            line=fo.readline()
    df = pd.DataFrame(table_rows, columns=["DATE","TIME","TIME-ZONE"," File name of ASA","Sequence and protocol type of the incident ","IP1","FOR","IP2A","TO","IP2B"])
    print(df)
    if location2 != "NO" :
        df.to_excel(location2)