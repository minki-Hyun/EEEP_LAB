import pandas as pd
import numpy as np
import IO_Analysis_lib as ioa
# # 원하는 부문이 대분류속 몇개인지 확인
url = "C:\\PythonWorkspace\\Lab_code\\IO Analysis\\2015_부문분류표.xlsx"
url1 = "C:\\PythonWorkspace\\Lab_code\\IO Analysis\\투입산출표_생산자가격_기본부문.xlsx"

url_home = "C:\\PythonWorkspace\\EEEP_LAB\\IO Analysis\\2015_부문분류표.xlsx"
url1_home = "C:\\PythonWorkspace\\EEEP_LAB\\IO Analysis\\투입산출표_생산자가격_기본부문.xlsx"


# # file = pd.read_excel(url, sheet_name="상품분류표",header = 1, usecols=["기본부문(381)","대분류(33)"])
# # file = file.iloc[1:,:]
# # file = file.dropna(axis=0,how = 'all')
# # b= list(file.count())
# # print("b=",b)

# # print(file)
# # a = {"기본부문(381)":["flag_a"],"대분류(33)":["flag_b"]}
# # a = pd.DataFrame(a,columns=["기본부문(381)","대분류(33)"])
# # print(a)

# # # 나중에 for문 돌릴 때 마지막 false 안나오는거 고쳐줌
# # file = pd.concat([file,a], axis = 0, ignore_index=True)
# # print(file)
# # file = pd.isnull(file)
# # file = file.to_numpy()
# # rows, columns = file.shape

# # j = 1
# # li = []

# # for i in range(1, rows):
    
# #     if file[i,1]==False:
# #         li.append(j)
# #         j = 1
# #     else:
# #         j+=1

    
# # print (li,type(li[0]))

# #1. 대분류 하나에 기본부문 몇개인지
    
# file = pd.read_excel(url, sheet_name="상품분류표",header = 1, usecols=["기본부문(381)","대분류(33)"])
# # format(str.__contains__(self, o))
# file = file.iloc[1:,:]
# print(file)
# file_a = file.dropna(axis=0,how = 'all')
# b= list(file_a.count())
# large_z_sizenum = b[1]
# small_z_sizenum = b[0]

# # 나중에 for문 돌릴 때 마지막 false 안나오는거 고쳐줌
# a = {'기본부문(381)' : ['flag_a'], '대분류(33)' : ['flag_b']}
# a = pd.DataFrame(a,columns=["기본부문(381)","대분류(33)"])
# file_b = pd.concat([file_a,a], axis = 0, ignore_index=True)

# file_b = pd.isnull(file_b)
# file_b = file_b.to_numpy()
# rows, columns = file_b.shape

# j = 1
# li = []

# for i in range(1, rows):
    
#     if file_b[i,1]==False:
#         li.append(j)
#         j = 1
#     else:
#         j+=1

#  #2. 내가  선택한 부문이 몇번째이며, 대분류 어디에 속하는지
    
# flag_sep1 = list(input("분석하고자 하는 산업의 코드를 입력하세요:\n").split())
# flag_sep2 = list(input("분석하고자 하는 산업이 속한 대분류 코드를 입력하세요:\n").split())
# sel_business = []
# sel_business_lar = []

# file_a_a = file_a.iloc[:,0].to_numpy()

# for i in range(0,len(flag_sep1)):
#     a= np.where(file_a_a==flag_sep1[i])
#     a= a[0]
#     b= a[0]
#     sel_business.append(b)

# file_a_b = file_a.iloc[:,1].dropna()#nan값 제거
# file_a_b = file_a_b.to_numpy()

# for j in range(0,len(flag_sep2)):
#     a= np.where(file_a_b == flag_sep2[j])
#     a= a[0]
#     b= a[0]
#     sel_business_lar.append(b)
    
# # return li,large_z_sizenum,small_z_sizenum,int(sel_business)+1,int(sel_business_lar)+1

# print(sel_business,sel_business_lar)

# #================================================================================================================위까지 성공
# #================================================================================================================위까지 성공
# #================================================================================================================위까지 성공
# #================================================================================================================위까지 성공

    
# #통합행렬 시작
# s_mat = np.zeros((large_z_sizenum + 1,small_z_sizenum))

# a0 = 0

# for i in range(0, large_z_sizenum):
#     b0 = a0 + li[i]

#     for j in range(a0,b0):
#         s_mat[i,j] = 1
    
#     a0 += li[i]

# for i in range(0,len(sel_business_lar)):
#     for j in range(0,len(sel_business)):
#         s_mat[sel_business_lar[i],sel_business[j]] = 0
#         s_mat[large_z_sizenum,sel_business[j]] = 1

# print(s_mat)


# 기본부문 취업유발효과 구하기

# # 기본부문이 소분류속 몇개인지 세기
# file = pd.read_excel(url, sheet_name="상품분류표",header = 1, usecols=["기본부문(381)","소분류(165)"])
# file = file.iloc[1:,:]
# file_title = list(file.columns)
# flag_dic = {}
# for i in range(len(file_title)):
#     flag_dic[file_title[i]] = "flag_{}".format(i)
# flag_dic = pd.DataFrame([flag_dic])
# file_b = pd.concat([file,flag_dic], axis = 0, ignore_index=True)
# file_b = file_b.isna()
# file_b = file_b.to_numpy()
# # print(len(file_b))
# li = []
# j = 1

# for i in range(1,file_b.shape[0]):
#     if file_b[i,1]==False:
#         li.append(j)
#         j = 1
    
#     else:
#         j+=1

# print("li")
# print(li)
# print()

# io_mat_a = pd.read_excel(url1,sheet_name="A표_국산거래표(생산자)", header=5, index_col=1, skipfooter=1)
# io_mat_a = io_mat_a.loc[:,"총수요계"].to_numpy()
# print("io_mat_a")
# print(io_mat_a)
# print()
# li1 = []
# a0=0
# for i in range(0,len(li)):
#     sum0 = 0
#     for j in range (a0 , a0+li[i]):
#         sum0 += io_mat_a[j]
#     li1.append(sum0)
#     a0 += li[i]

# print(li1)

# io_mat_employ = pd.read_excel(url1,sheet_name="취업자수 및 피용자수(상품)",index_col=0,skipfooter=1)
# flag_em = io_mat_employ.to_numpy() / np.array(li1).reshape(len(li1),1)

# print("flag_em")
# print(flag_em)
# print()

# io_mat_b = np.array([])
# a0 = 0  
# for i in range(0,len(flag_em)):
#     for j in range (a0, a0+li[i]):
#         io_mat_b=np.append(io_mat_b,io_mat_a[j]*flag_em[i])
#     a0 += li[i]
# print(len(io_mat_b))

# # 실제로 맞는지 확인해야 함

s_mat = ioa.func_integrated_matrix(url,sep_li,large_z_sizenum,small_z_sizenum,sel_business,sel_business_lar) # 4,1도 자동화?

io_mat_a = pd.read_excel(url1,sheet_name="A표_국산거래표(생산자가격)", header=5, index_col=1, skipfooter=1)
io_mat_a = io_mat_a.loc[:,"수출"].to_numpy()
io_mat_b = io_mat_a @ s_mat.transpose()
io_mat_a_coeff = io_mat_a / total_demand


print(io_mat_a)