import requests
import json 
import csv
import os
import time
import pandas as pd
import math

def category_collection():
    
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
               "Content-Type": "application/json"
              }
    print("请输入你的供应商编号（799是瑞舒，1697是荣满，2092是苏铖粤）")
    supplier = str(input())
    payload = {"supplierId":supplier}
    url = "https://www.rjmart.cn/gaea/detail/category"
    web = requests.post(url,headers =headers,data = json.dumps(payload))
    data_json = json.loads(web.text)
    data = data_json.get("data")
    zidian = {}
    BIG_LIST = []
    
    for i in data:
        big_lei = i.get("id")
        big_name = i.get("name")
        BIG_LIST.append(str(big_lei))
        zidian[str(big_lei).strip()] = big_name
        for j in i["subList"]:
            xiaolei = str(j.get("id")).strip()
            zidian[xiaolei] = big_name    
    
    DATA.append(BIG_LIST)
    DATA.append(zidian)
    DATA.append(supplier)


def data_collection():
    com_id = str(DATA[2])
    print("请输入你要保存的文件名字")
    name = input()
    name = name +".csv"
    count = 0

    for i in range(1,26):
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
                   "Content-Type": "application/json"
                  }

        payload_suoyou = {"brandIds":[],"brandName":"","casNo":"","city":"","orgId":"","pageSize":20,"pageNo":i,"sort":1,"key":"","maxPrice":"","minPrice":"","categoryIds":[],"searchFlag":11,"supplierIds":[com_id],"supplierName":"","flag":10}
        url = "https://www.rjmart.cn/gaea/search"
        web = requests.post(url,headers =headers,data = json.dumps(payload_suoyou))
        data_json = json.loads(web.text)
        data_all = data_json.get("data").get("products")

        with open(name,"a",newline = "",encoding = "utf-8")as q:
                fieldnames = list(set(data_all[0]))
                writer = csv.DictWriter(q,fieldnames = fieldnames)
                if count == 0:
                    writer.writeheader()
                    writer.writerows(data_all)
                    count +=1
                else:
                    writer.writerows(data_all)
                    count +=1
        print("当前录入全部类别的数据为第{}页".format(count))
        time.sleep(1)
    
    for j in DATA[0]:
        page = 1
        total_page= 1
        count = 0
        try:
            while page <= total_page :
                payload_cateid = {"brandIds":[],"brandName":"","casNo":"","city":"","orgId":"","pageSize":20,"pageNo":page,"sort":1,"key":"","maxPrice":"","minPrice":"","categoryIds":[j],"searchFlag":11,"supplierIds":[com_id],"supplierName":"","flag":10}
                web_id = requests.post(url,headers =headers,data = json.dumps(payload_cateid))

                data_json_id = json.loads(web_id.text)#
                data_id = data_json_id.get("data").get("products")
                with open(name,"a",newline = "",encoding = "utf-8")as n:
                    fieldnames = list(set(data_id[0]))
                    writer = csv.DictWriter(n,fieldnames = fieldnames)
                    writer.writerows(data_id)
                count +=1
                print("当前录入数据为大类{}的第{}页".format(DATA[1][j],count))
                time.sleep(2)#

                total = data_json_id.get("total")
                total_page = math.ceil(total//20)                
                page += 1
        except:
            print("当前录入失败数据为大类{}的第{}页".format(DATA[1][j],count))
    DATA.append(name)

def data_processing():
    df = pd.read_csv(DATA[3])
    z = df[["categoryId","name","brandName","specification","productNum","price"]]
    z = z.drop_duplicates()
    z_types = {"categoryId":str}
    z = z.astype(z_types)
    z = z.replace(DATA[1])
    z.to_excel("./suchengyue/result.xlsx",index = False)
    dalei_name = z["categoryId"].unique() 
    for i in dalei_name:
        data_z = z[z["categoryId"] == i]
        q = i.replace("/","_").strip()
        path ="."+"/suchengyue/ " +  q + ".xlsx"
        data_z.to_excel(path,index = False)


def main():
    category_collection()
    data_collection()
    data_processing()

#DATA第0个是公司的大类列表，第1个是该公司所有类的大类归属字典，第2个是供应商编号，第3个是保存的文件名
DATA=[]
main()
