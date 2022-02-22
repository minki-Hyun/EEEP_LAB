import numpy as np
import pandas as pd

#=============================================================================================================================================================================
# 엑셀 불러오기

def func_Load_excel(url):
    io_mat_a = pd.read_excel(url,sheet_name="A표_국산거래표(생산자가격)", header=5, index_col=1)
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

# 통합행렬 만들기

def func_integrated_matrix (large_z_sizenum,small_z_sizenum, sel_business, sel_business_lar):
#앞의 변수 2개는 "갯수" 기준(Ex:34개), 뒤의 변수 2개는 "인덱스"기준 : 이름이랑 일치하느냐로 뽑을 거임
    print("선택하신 부문을 대분류 기준으로 통합합니다.\n하나의 대분류안에 몇 개의 부문이 있나요?.\n\nEX)\n(수산업 화력 수력)=대분류 1\n(농업,광산업)=대분류2라면 입력:2 3\n")
    
    sep_category = list(input().split())
    sep_category = list(map(int,sep_category))
    s_mat = np.zeros((large_z_sizenum + 1,small_z_sizenum))

    a0 = 0

    for i in range(0, large_z_sizenum):
        b0 = a0 + sep_category[i]

        for j in range(a0,b0):
            s_mat[i,j] = 1
        
        a0 += sep_category[i]
    
    s_mat[sel_business_lar-1,sel_business-1] = 0
    s_mat[large_z_sizenum,sel_business-1] = 1

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
    io_mat_b = pd.read_excel(url,sheet_name="A표_총거래표(생산자가격)", header=5, index_col=1)
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
    
    #2. A 구하기
    A_mat = z_mat @ (np.linalg.inv(x_hat_mat))
    
    
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

def func_employ_coeff(url,s_mat,total_demand):
    
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

    # 2. 부가가치유발효과 구하기
    
    employ_eff = employ_hat @ prod_eff
    
    return pd.DataFrame(employ_eff)

#=============================================================================================================================================================================
#=============================================================================================================================================================================
#=============================================================================================================================================================================
#=============================================================================================================================================================================
#=============================================================================================================================================================================

#이 밑에부터는 처음에 짠것

# 엑셀 받기
def Load_excel(url):
    io_mat = pd.read_excel(url,sheet_name="A표_국산거래표(생산자)", header=5,usecols='B:')
    print (io_mat)


#=============================================================================================================================================================================

# 변수받기

def starting_program ():
    print("IO분석을 시작합니다.\n=====================================================================================")
    # 변수/ 파일 정의 : 바꿔야 할 부분
    while 1:
        analysis_type = input("분석하고자 하는 부문을 입력하세요.\n기본부문 - 1, 소분류 - 2, 중분류 - 3 : ")
        

        if analysis_type == "1" :
            z_sizenum = int(input("국산거래표(생산자가격)의 기본부문 갯수를 입력하세요 : "))
            large_z_sizenum = int(input("국산거래표(생산자가격)의 대분류 갯수를 입력하세요 : "))
            sel_business = list(input("분석하실 기본부문의 이름을 입력하세요.(부문이 여러개라면 띄워쓰기를 포함하여 연속으로 입력하세요.)\nEX)화력 수력"))
            sel_business_lar = list(input("분석하실 기본부문이 속해있는 대분류의 이름을 입력하세요.(부문이 여러개라면 띄워쓰기를 포함하여 연속으로 입력하세요.)\nEX)화력 수력"))
            break
        
        elif analysis_type == "2" :
            z_sizenum = int(input("국산거래표(생산자가격)의 소분류 갯수를 입력하세요 : "))
            large_z_sizenum = int(input("국산거래표(생산자가격)의 대분류 갯수를 입력하세요 : "))
            sel_business = list(input("분석하실 기본부문의 이름을 입력하세요.(부문이 여러개라면 띄워쓰기를 포함하여 연속으로 입력하세요.)\nEX)화력 수력"))
            sel_business_lar = list(input("분석하실 기본부문이 속해있는 대분류의 이름을 입력하세요.(부문이 여러개라면 띄워쓰기를 포함하여 연속으로 입력하세요.)\nEX)화력 수력"))
            break
        
        elif analysis_type == "3" :
            z_sizenum = int(input("국산거래표(생산자가격)의 중분류 갯수를 입력하세요 : "))
            large_z_sizenum = int(input("국산거래표(생산자가격)의 대분류 갯수를 입력하세요 : "))
            sel_business = list(input("분석하실 기본부문의 이름을 입력하세요.(부문이 여러개라면 띄워쓰기를 포함하여 연속으로 입력하세요.)\nEX)화력 수력"))
            sel_business_lar = list(input("분석하실 기본부문이 속해있는 대분류의 이름을 입력하세요.(부문이 여러개라면 띄워쓰기를 포함하여 연속으로 입력하세요.)\nEX)화력 수력"))
            break
        
        else : 
            print("오류! 1,2,3을 제외한 숫자 또는 다른 문자를 입력했을 수 있습니다. 다시 입력하세요.")

    print("분석하기를 원하는 산업을 입력하세요.이때 갯수가 여러개라면, 띄어쓰기를 포함하세요.\nEX)수산업 화력 수력")
    list1 = list(input().split())
    return list1, z_sizenum, large_z_sizenum, sel_business, sel_business_lar
