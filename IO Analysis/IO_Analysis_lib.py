import numpy as np
import pandas as pd

#=============================================================================================================================================================================
# IO 엑셀 불러오기

def func_Load_excel(url):
    io_mat_a = pd.read_excel(url,sheet_name="A표_국산거래표(생산자)", header=5, index_col=1)
    io_mat_a = io_mat_a.drop(io_mat_a.columns[0], axis=1)
    io_mat_a = io_mat_a.iloc[:-1,:] # 뒤에서부터 1행
    #국산거래표 그대로 들고 옴

    io_mat = io_mat_a.iloc[:,:-10]
    #뒤에서부터 10열 삭제. 이때 iloc 대신 loc 쓰면 오류남 : loc는 라벨로 받음 "기타" 이런 식으로

    column_list = list(io_mat.columns.values)
    rows_list = list(io_mat.index.values)
    
    io_mat = io_mat.replace(" ","", regex=True) # regex : 부분일치 여부, False면 전체 일치
    io_mat = io_mat.replace("\\n","", regex=True)

    # io_mat = io_mat_raw.drop(["중간수요계","최종수요계","총수요계"],axis=1)
    return io_mat,io_mat_a,column_list,rows_list

#=============================================================================================================================================================================

# 부문분류표 들고와서 대분류 하나에 기본부문 몇개인지

def func_sep (url):

#1. 대분류 하나에 기본부문 몇개인지
    
    wd = input("선택하신 상품의 분류를 입력해주세요, Ex)기본부문: \n").replace(" ","")
    file = pd.read_excel(url, sheet_name="상품분류표",header = 1)

    # 기본부문, 중분류 상관없이 받아올 수 있도록 하기
    title_list = list(file.columns.values)
    title_flag1 = []
    title_flag2 = []
    
    for i in range(len(title_list)):
        if (wd in title_list[i])|("대분류" in title_list[i]):
            title_flag1.append(i)
            title_flag2.append(title_list[i])

    file = file.iloc[1:,title_flag1]
    print(file)
    file_a = file.dropna(axis=0,how = 'all')
    b= list(file_a.count())
    large_z_sizenum = b[1]
    small_z_sizenum = b[0]

    # 나중에 for문 돌릴 때 마지막 false 안나오는거 고쳐줌
    a = {}
    for j in range(len(title_flag2)):
        a[title_flag2[j]] = "flag_{}".format(j)
    a = pd.DataFrame([a])
    print(a)

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

    return wd,li,large_z_sizenum,small_z_sizenum,sel_business,sel_business_lar

#=============================================================================================================================================================================

# 통합행렬 만들기

def func_integrated_matrix (url1,li,large_z_sizenum,small_z_sizenum, sel_business, sel_business_lar):
    
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

    return s_mat

#=============================================================================================================================================================================

# 재통합된 산업연관표

def func_new_table(s_mat,io_mat):
    
    sz_mat = s_mat@io_mat
    z_mat = sz_mat @ np.transpose(s_mat)
    
    return z_mat


#=============================================================================================================================================================================

# 총 수요 구하기 ( = 총 투입)

def func_total_demand(s_mat, demand_in_iomat,z_mat, large_z_sizenum):
    
    demand1 = pd.DataFrame(s_mat @ demand_in_iomat)
    demand2 = (z_mat @ np.ones((large_z_sizenum +1 , 1)).astype(int))
    
    total_demand =  demand1 + demand2
    
    return total_demand

#=============================================================================================================================================================================

# 부가가치계수 구하기

def func_added_value(url,s_mat,z_mat,total_demand):
    
    #부가가치계 불러오기
    io_mat_b = pd.read_excel(url,sheet_name="A표_총거래표(생산자)", header=5, index_col=1)
    io_mat_b = io_mat_b.drop(io_mat_b.columns[0], axis=1)
    io_mat_b = io_mat_b.loc["부가가치계",:]
    io_mat_b = pd.DataFrame(io_mat_b.dropna())
    io_mat_b = io_mat_b.iloc[:-1,:]

    #불러온 부가가치계를 34부문으로 확장
    added_value_mat = np.transpose(io_mat_b) @ np.transpose(s_mat)
    added_value_mat = np.transpose(added_value_mat)

    total_demand.columns = ["부가가치계"]
    
    #각 요소를 총 투입으로 나누기
    added_value_var = (added_value_mat / total_demand)
    added_value_var.round(9)
    added_value_var.columns = ["부가가치계수"]

    return added_value_var

#=============================================================================================================================================================================

# 생산유발계수 구하기

def func_prod_coeff (large_z_sizenum, z_mat, total_demand):
    
    #1. x_hat 구하기
    x_hat_mat = np.zeros((large_z_sizenum+1,large_z_sizenum+1))
    total_demand = total_demand.to_numpy()
    
    for i in range(0,large_z_sizenum+1):
        x_hat_mat[i,i] = total_demand[i,0]
    
    x_hat_mat_inv = np.linalg.inv(x_hat_mat)
    #2. A 구하기
    A_mat = z_mat @ x_hat_mat_inv
    
    #3. 생산유발계수 = prod_var_mat (레온티예프 역행렬) : (I-A)^(-1)
    prod_var_mat = np.linalg.inv(np.eye(large_z_sizenum+1) - A_mat)
    

    return pd.DataFrame(prod_var_mat),pd.DataFrame(A_mat)

#=============================================================================================================================================================================

#생산유발효과 {(I-A)^(-1)} * A의 마지막 열

def func_prod_eff (prod_coeff, A_mat):
    # prod_coeff=prod_coeff.to_numpy()
    # A_mat = A_mat.to_numpy
    prod_coeff_a = prod_coeff.iloc[:-1,:-1]
    A_mat_a = A_mat.iloc[:-1,-1]
    prod_eff = prod_coeff_a @ A_mat_a
    
    return prod_eff

#=============================================================================================================================================================================

# 부가가치유발효과

def func_added_eff (large_z_sizenum,prod_eff,added_value):

    # 1. 부가가치 유발계수_hat 구하기
    
    added_value = added_value.to_numpy()
    added_value_hat = np.zeros((large_z_sizenum,large_z_sizenum))

    for j in range(0,large_z_sizenum-1):
        added_value_hat[j,j] = added_value[j,0]
    
    # 2. 부가가치유발효과 구하기
    
    add_value_eff = added_value_hat @ prod_eff

    return pd.DataFrame(add_value_eff)

#=============================================================================================================================================================================

# 취업유발계수 구하기

def func_employ_coeff(wd,url,url1,s_mat,total_demand):
    
    if "기본부문" in wd:
        employ_coeff_a = pd.read_excel(url,sheet_name="취업자수 및 피용자수(상품)_해당분류",index_col=0,skipfooter=1)
        file = pd.read_excel(url1, sheet_name="상품분류표",header = 1, usecols=["기본부문(381)","소분류(165)"])
        



    else:
        #1. 취업인원 추출
        employ_coeff_a = pd.read_excel(url,sheet_name="취업자수 및 피용자수(상품)_해당분류",index_col=0,skipfooter=1)
        employ_coeff_a = employ_coeff_a.to_numpy()
        employ_coeff_b = s_mat @ employ_coeff_a
        
        #2. 취업유발계수 구하기 (취업인원 / (총수요/1000) : 10억당 취업인원 수)
        
        total_demand = total_demand.to_numpy()
        employ_coeff_c = employ_coeff_b / (total_demand / 1000)




    return pd.DataFrame(employ_coeff_c)

#=============================================================================================================================================================================

# 취업유발효과 구하기
def func_employ_eff(large_z_sizenum, prod_eff,employ_coeff):
    
    #1. 취업유발계수_hat 구하기
    
    employ_coeff = employ_coeff.to_numpy()
    employ_hat = np.zeros((large_z_sizenum,large_z_sizenum))

    for j in range(0,large_z_sizenum-1):
        employ_hat[j,j] = employ_coeff[j,0]

    # 2. 취업유발효과 구하기
    
    employ_eff = employ_hat @ prod_eff
    
    return pd.DataFrame(employ_eff)