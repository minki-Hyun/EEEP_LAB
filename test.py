import pandas as pd
import numpy as np

# # 원하는 부문이 대분류속 몇개인지 확인
url = "C:\\PythonWorkspace\\Lab_code\\IO Analysis\\2015_부문분류표.xlsx"
url1 = "C:\\PythonWorkspace\\Lab_code\\IO Analysis\\투입산출표_생산자가격_기본부문.xlsx"

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

#1. 대분류 하나에 기본부문 몇개인지
    
file = pd.read_excel(url, sheet_name="상품분류표",header = 1, usecols=["기본부문(381)","대분류(33)"])
# format(str.__contains__(self, o))
file = file.iloc[1:,:]
print(file)
file_a = file.dropna(axis=0,how = 'all')
b= list(file_a.count())
large_z_sizenum = b[1]
small_z_sizenum = b[0]

# 나중에 for문 돌릴 때 마지막 false 안나오는거 고쳐줌
a = {'기본부문(381)' : ['flag_a'], '대분류(33)' : ['flag_b']}
a = pd.DataFrame(a,columns=["기본부문(381)","대분류(33)"])
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

 #2. 내가  선택한 부문이 몇번째이며, 대분류 어디에 속하는지
    
flag_sep1 = list(input("분석하고자 하는 산업의 코드를 입력하세요:\n").split())
flag_sep2 = list(input("분석하고자 하는 산업이 속한 대분류 코드를 입력하세요:\n").split())
sel_business = []
sel_business_lar = []

file_a_a = file_a.iloc[:,0].to_numpy()

for i in range(0,len(flag_sep1)):
    a= np.where(file_a_a==flag_sep1[i])
    a= a[0]
    b= a[0]
    sel_business.append(b)

file_a_b = file_a.iloc[:,1].dropna()#nan값 제거
file_a_b = file_a_b.to_numpy()

for j in range(0,len(flag_sep2)):
    a= np.where(file_a_b == flag_sep2[j])
    a= a[0]
    b= a[0]
    sel_business_lar.append(b)
    
# return li,large_z_sizenum,small_z_sizenum,int(sel_business)+1,int(sel_business_lar)+1

print(sel_business,sel_business_lar)

#================================================================================================================위까지 성공
#================================================================================================================위까지 성공
#================================================================================================================위까지 성공
#================================================================================================================위까지 성공

    
#통합행렬 시작
s_mat = np.zeros((large_z_sizenum + 1,small_z_sizenum))

a0 = 0

for i in range(0, large_z_sizenum):
    b0 = a0 + li[i]

    for j in range(a0,b0):
        s_mat[i,j] = 1
    
    a0 += li[i]

for i in range(0,len(sel_business_lar)):
    for j in range(0,len(sel_business)):
        s_mat[sel_business_lar[i],sel_business[j]] = 0
        s_mat[large_z_sizenum,sel_business[j]] = 1

print(s_mat)