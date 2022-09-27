from operator import indexOf
from sre_compile import isstring
# import string
# from xmlrpc.client import DateTime
# import pandas as pd
import arabic_reshaper
# from bidi.algorithm import get_display
import xlrd     
# import openpyxl
import pandas as pd
from openpyxl import load_workbook
# # read by default 1st sheet of an excel file
Efile = pd.ExcelFile('arb.xlsx')
print(Efile.sheet_names)
z=Efile.parse(Efile.sheet_names[0]);
print(z);

# dat=pd.DataFrame()
# pip install name
with pd.ExcelWriter('test.xlsx', engine='openpyxl', mode='a') as writer: 
        z.to_excel(writer,sheet_name="aaa",index=[])

# print(Efile);
lst=[]
for index, rows in z.iterrows():
        # Create list for the current row
        my_list =rows.values.tolist()
        if(not isstring(my_list[0])):continue
        if( not (my_list[0][0]>='A' and my_list[0][0]<='z')):
                my_list[0]= arabic_reshaper.reshape(my_list[0])[::-1]
        if( not( my_list[1][0]>='A' and my_list[1][0]<='z')):
                my_list[1]= arabic_reshaper.reshape(my_list[1])[::-1]
        if( not(my_list[3][0]>='A' and my_list[3][0]<='z')):
                my_list[3]= arabic_reshaper.reshape(my_list[3])[::-1]
        # #append the list to the final list
        lst.append(my_list)
# Print the list
print(lst)
# path = 'test.xlsx'
# dataframe1.to_excel(path,sheet_name="sheetxyz")

