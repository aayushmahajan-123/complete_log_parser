#install regex , pandas , numpy
import pandas as pd
import re
import numpy as np
import fortigate as ft
import server_access as sa
import cisco_asa as ca


def main():
    print("ENTER THE FILE LOCATION---->>")
    location=input()
    print("ENTER THE TYPE OF LOG----->>")
    print("1>SERVER_ACCESS,2>FORTIGATE300D,3>CISCO_ASA")
    choice=int(input())
    print("ENTER THE DESTINATION LOCATION(enter 'NO' if excel not required---->")
    location2=input()
    if choice==2:
        ft.parse_fortigate(location,location2)
    elif choice==1:
        sa.parse_server_access(location,location2)
    elif choice==3:
        ca.parse_cisco(location,location2)
    else:
        print("INVALID ARGUMENTS,PLEASE TRY AGAIN")

if __name__=="__main__":
    main()

