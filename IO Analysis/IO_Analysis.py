import numpy as np
import pandas as pd
import IO_Analysis_lib as ioa

url_base = input("폴더 경로를 입력하시오:\n")
url_excel_io = input("분석하고자 하는 산업연관표의 파일 이름을 입력하시오:\n")
url_excel_sep = input("분석하고자 하는 산업연관표의 부문분류표 파일 이름을 입력하시오:\n")

url = url_base+"\\"+url_excel_io # IO분석 파일 있는 위치
url1 = url_base+"\\"+url_excel_sep # 부문분류표 파일 있는 위치

sh_name_rawio = input("IO분석에 필요한 '국산거래표'의 시트이름을 복사하세요.\n주의! 반드시 시트 이름을 '복사' 후 붙여넣으셔야 합니다: ") # 국산거래표 시트 이름
sh_name_totalio = input("IO분석에 필요한 '총거래표'의 시트이름을 복사하세요.\n주의! 반드시 시트 이름을 '복사' 후 붙여넣으셔야 합니다: ") # 총거래표 시트 이름
sh_name_distribution = input("IO분석에 필요한 '부문분류표'의 시트이름을 복사하세요.\n주의! 반드시 시트 이름을 '복사' 후 붙여넣으셔야 합니다: ") # 부문분류표 시트 이름
sh_name_employ = input("IO분석에 필요한 '고용표'의 시트이름을 복사하세요.\n주의! 반드시 시트 이름을 '복사' 후 붙여넣으셔야 합니다: ") # 고용표 시트 이름

# 부문 쪼개기
wd, sep_li, large_z_sizenum, small_z_sizenum, sel_business,sel_business_lar  = ioa.func_sep(url1,sh_name_distribution)

# io 엑셀 불러오기
io_mat, io_mat_raw, column_list, row_list = ioa.func_Load_excel(url,sh_name_rawio)

#통합 행렬 만들기
s_mat = ioa.func_integrated_matrix(url,sep_li,large_z_sizenum,small_z_sizenum,sel_business,sel_business_lar) # 4,1도 자동화?
print("통합행렬\n\n",s_mat,"\n")

# 재통합된 산출표 만들기
z_mat = ioa.func_new_table(s_mat,io_mat)
print("재통합된 산출표\n\n",z_mat,"\n")
print()

# 총 수요 구하기 (=총 투입)
total_demand = ioa.func_total_demand(s_mat,io_mat_raw.loc[:,"최종수요계"],z_mat,large_z_sizenum)
print("총 수요 (= 총 투입)\n\n",total_demand,"\n")
# demand_in_iomat = io_mat_raw.loc[:,"최종수요계"] 이거 한번에 줄인거임

# # 부가가치계수 구하기
added_value = ioa.func_added_value(url,sh_name_totalio,s_mat,z_mat,total_demand)
print("부가가치계수\n",added_value,"\n\n")

# 생산유발계수 구하기
prod_coeff, A_mat = ioa.func_prod_coeff(large_z_sizenum,z_mat,total_demand)
print("생산유발계수\n",prod_coeff,"\n\n")

#생산유발효과 구하기
prod_eff = ioa.func_prod_eff(prod_coeff,A_mat)
print("생산유발효과\n",prod_eff,"\n\n")

# 부가가치유발효과
add_eff = ioa.func_added_eff(large_z_sizenum, prod_eff, added_value)
print("부가가치유발효과\n", add_eff, "\n\n")

# 취업유발계수 구하기
employ_coeff = ioa.func_employ_coeff(wd, url, url1, s_mat, total_demand,sh_name_distribution,io_mat_raw,sh_name_employ)
print("취업유발계수\n",employ_coeff,"\n\n")

# 취업유발효과 구하기
employ_eff = ioa.func_employ_eff(large_z_sizenum, prod_eff, employ_coeff)
print("취업유발효과\n",employ_eff,"\n\n")

# 수출유발계수 구하기
export_coeff = ioa.func_export(url, s_mat, total_demand,io_mat_raw)
print("수출유발계수\n",export_coeff,"\n\n")

# 수출유발효과 구하기
export_eff = ioa.func_export_eff(export_coeff, large_z_sizenum, prod_eff)
print("수출유발효과\n",export_eff,"\n\n")
