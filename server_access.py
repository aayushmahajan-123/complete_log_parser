import pandas as pd
import re
import numpy as np
import openpyxl


table_rows=[]

def parser(test_string):
    date_pattern="(?:20[0-9][0-9])\-(?:0[1-9]|1[0-2])\-(?:0[1-9]|1[0-9]|2[0-9]|3[0-1])"
    time_pattern="T(?:0[0-9]|1[0-9]|2[0-3])\:(?:[0-5][0-9])\:(?:[0-5][0-9])"
    timezone_pattern="[\+\-](?:0[0-9]|1[0-3])\:(?:00|30|45)"
    ipaddresses_pattern="(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])"
    accessdate_pattern="(?:0[1-9]|[12][0-9]|3[01])/(?:[a-zA-Z]{3})/(?:20[0-9][0-9])"
    accesstime_pattern="[:](?:\d\d)[:](?:\d\d)[:](?:\d\d)"
    httpmethod_pattern="GET|POST"
    httpversion_pattern="HTTP/\d.\d\s\d+\s.+"
    hostname_pattern="[a-z]+[0-9]*\s"
    app_profile_pattern="[a-z]+[0-9]*\-[a-z]+[\:]*"
    uri_pattern="\s[/].+[/].+HTTP"
    xyz_pattern = "(?:(?:[a-zA-Z0-9]+\:){7})(?:[a-zA-Z0-9]+)"


    newrow=[]
    date=re.findall(date_pattern,test_string)
    if date:
        newrow.append(date[0])
    elif date==None:
        return

    time=re.findall(time_pattern,test_string)
    if time:
        xtime=time[0]
        xtime=xtime[1:]
        newrow.append(xtime)

    timezone=re.findall(timezone_pattern,test_string)
    if timezone:
        newrow.append(timezone[0])

    hostname=re.findall(hostname_pattern,test_string)
    if hostname:
        newrow.append(hostname[0])
    app_profile=re.findall(app_profile_pattern,test_string)
    if app_profile :
        newrow.append(app_profile[0])
    else:
        newrow.append("-")

    ipadd=re.findall(ipaddresses_pattern,test_string)
    if len(ipadd)<3 :
        while len(ipadd)<3 :
            ipadd.append("-")
    newrow.append(ipadd[0])
    newrow.append(ipadd[1])
    newrow.append(ipadd[2])

    xyz=re.findall(xyz_pattern,test_string)
    if xyz:
        xyz=xyz[0]
        newrow.append(xyz)
    else:
        newrow.append("-")

    accessdate=re.findall(accessdate_pattern,test_string)
    if accessdate:
        newrow.append(accessdate[0])

    accesstime=re.findall(accesstime_pattern,test_string)
    if accesstime:
        temp_time=accesstime[0]
        temp_time=temp_time[1:]
        newrow.append(temp_time)

    uri=re.findall(uri_pattern,test_string)
    xyz=re.findall(xyz_pattern,test_string)
    if uri:
        uri=uri[0].split(" ")[1]
        newrow.append(uri)
    else :
        newrow.append("-")


    httpmethod=re.findall(httpmethod_pattern,test_string)
    if httpmethod:
        newrow.append(httpmethod[0])

    httpversion=re.findall(httpversion_pattern,test_string)
    if httpversion:
        httpversion=httpversion[0].split(" ")
        newrow.append(httpversion[0])
        newrow.append(httpversion[1])
        newrow.append(httpversion[2])
    y=test_string.split(" ")
    newrow.append(y[-1])

    table_rows.append(newrow)


def parse_server_access(location1,location2):
    #str="2019-12-30 T16:31:29 +05:30 prdserb02 asean-access: 120.29.85.71   10.10.36.230 10.10.36.13 - - [30/Dec/2019:16:31:21 +0530]  GET /ASEAN/resources/app_srv/asean/global/js/bootstrap.min.js HTTP/1.1 200 37045 Mozilla/5.0 (Linux; Android 8.1.0; Redmi 5 Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/79.0.3945.93 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/251.0.0.31.111;] https://aistic.gov.in/ASEAN/aistdfFellowship"
    #parser(str)
    #for i in table_rows:
    # print(i)
    #with open(r"E:\cdac\prdserb02.log.txt",'r') as fo:
    #with open(r"H:\CDAC\SERVER\prdserb02.log.txt",'r') as fo:
    with open(location1,'r') as fo:
        line=fo.readline()
        line=fo.readline()
        while line:
            parser(line)
            line=fo.readline()

    df=pd.DataFrame(table_rows,columns=['DATE','TIME','TIMEZONE','HOST-NAME','APP-PROFILE','SOURCE-IP','LB-IP','DEST-IP','ADDRESS','ACCESS-DATE','ACCESS-TIME','URI','HTTP-METHOD','HTTP-VERSION','RESPONSE-CODE','SIZE','URL'])
    print(df)

    if location2 != "NO" :
        df.to_excel(location2)
