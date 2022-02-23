import pandas as pd
import numpy as np

# # 원하는 부문이 대분류속 몇개인지 확인
url = "C:\\PythonWorkspace\\Lab_code\\IO Analysis\\2015_부문분류표.xlsx"

# file = pd.read_excel(url, sheet_name="상품분류표",header = 1, usecols=["기본부문(381)","대분류(33)"])
# file = file.iloc[1:,:]
# file = file.dropna(axis=0,how = 'all')
# b= list(file.count())
# print("b=",b)

# print(file)
# a = {"기본부문(381)":["flag_a"],"대분류(33)":["flag_b"]}
# a = pd.DataFrame(a,columns=["기본부문(381)","대분류(33)"])
# print(a)

# # 나중에 for문 돌릴 때 마지막 false 안나오는거 고쳐줌
# file = pd.concat([file,a], axis = 0, ignore_index=True)
# print(file)
# file = pd.isnull(file)
# file = file.to_numpy()
# rows, columns = file.shape

# j = 1
# li = []

# for i in range(1, rows):
    
#     if file[i,1]==False:
#         li.append(j)
#         j = 1
#     else:
#         j+=1

    
# print (li,type(li[0]))

file = pd.read_excel(url, sheet_name="상품분류표",header = 1, usecols=["중분류(83)","대분류(33)"])
# format(str.__contains__(self, o))
file = file.iloc[1:,:]
file_a = file.dropna(axis=0,how = 'all')
b= list(file_a.count())
large_z_sizenum = b[1]
small_z_sizenum = b[0]

# 나중에 for문 돌릴 때 마지막 false 안나오는거 고쳐줌
a = {'중분류(83)' : 'flag_a', '대분류(33)' : ['flag_b']}
a = pd.DataFrame(a,columns=["중분류(83)","대분류(33)"])
file_b = pd.concat([file_a,a], axis = 0, ignore_index=True)

file_b = pd.isnull(file_b)
file_b = file_b.to_numpy()
rows, columns = file_b.shape

j = 1
li = []

for i in range(1, rows):
    
    if file_b[i,1]==False:
        li.append(j)
        j = 1
    else:
        j+=1

print(li,large_z_sizenum,small_z_sizenum)

#2. 내가  선택한 부문이 몇번째이며, 대분류 어디에 속하는지

flag_sep1 = input("분석하고자 하는 산업의 코드를 입력하세요:\n")
flag_sep2 = input("분석하고자 하는 산업이 속한 대분류 코드를 입력하세요:\n")

file_a_a = file_a.iloc[:,0].to_numpy()
sel_business = np.where(file_a_a == flag_sep1)
print(int(sel_business[0])+1)

file_a_b = file_a.iloc[:,1].dropna()#nan값 제거
file_a_b = file_a_b.to_numpy()
sel_business_lar = np.where(file_a_b == flag_sep2)
print(int(sel_business_lar[0]+1))



# sel_business_lar = file_a_b[file_a_b == flag_sep2].index

# print(sel_business,sel_business_lar)