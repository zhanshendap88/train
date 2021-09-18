# -*- coding: utf-8 -*-
import requests
import json
import csv
import os
import time
import pandas as pd
import math

def spyder():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Content-Type": "application/json"
        }
    url = "https://www.rjmart.cn/gaea/search"
    print("请输入你要搜索的供应商名字")
    spyder_name = input()
    total_page = 1
    o = 1
    try:
        while o <= total_page:
            payload_cateid = {"supplierName": spyder_name, "pageSize": 10, "pageNo": o, "sort": 0, "flag": 20}
            web_id = requests.post(url, headers=headers, data=json.dumps(payload_cateid))
            data_json_id = json.loads(web_id.text)  #
            data_id = data_json_id.get("data")
            total_pages = data_json_id.get("total")
            total_page = math.ceil(total_pages / 10)
            for i in data_id:
                print(str(i["supplierName"]).replace('<span style="color:#f00">', '').replace('</span>','') + " : " + str(i["supplierId"]))
                time.sleep(1)
            o += 1
    except:
        print("查不到该供应商")
        return

def category_collection():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Content-Type": "application/json"
        }
    print("---------------------------")
    print("\n请输入你的供应商编号")
    print("竞争对手：799 瑞舒，1697 荣满，2092 苏铖粤，1283 广州美仑，570 英潍捷基，2710 广州恒研")
    supplier = str(input())
    payload = {"supplierId": supplier}
    payload_yanzheng = {"brandIds": [], "brandName": "", "casNo": "", "city": "", "orgId": "", "pageSize": 20,
                        "pageNo": 1, "sort": "", "key": "", "maxPrice": "", "minPrice": "", "categoryIds": [],
                        "searchFlag": 10, "supplierIds": [supplier], "supplierName": "", "flag": 10}
    url_yanzheng = "https://www.rjmart.cn/gaea/search"
    web_yanzheng = requests.post(url_yanzheng, headers=headers, data=json.dumps(payload_yanzheng))
    data_json = json.loads(web_yanzheng.text)
    data = data_json.get("data").get("products")
    if data == []:
        print("此供应商无商品")
        return
    print("---------------------------")
    print(data[0]["supplierName"])
    print("目标公司是否正确（y/n）")
    panduan = input()
    if panduan == "n":
        return
    url = "https://www.rjmart.cn/gaea/detail/category"
    web = requests.post(url, headers=headers, data=json.dumps(payload))
    data_json = json.loads(web.text)
    data = data_json.get("data")
    zidian = {}
    BIG_LIST = []
    category_IDS = {}
    for i in data:
        if i["subList"] == []:
            category_IDS[str(i.get("id")).strip()] = i.get("name")
        else:
            for z in i["subList"]:
                category_IDS[str(z.get("id")).strip()] = z.get("name")
        big_lei = i.get("id")
        big_name = i.get("name")
        BIG_LIST.append(str(big_lei))
        zidian[str(big_lei).strip()] = big_name
        for j in i["subList"]:
            xiaolei = str(j.get("id")).strip()
            zidian[xiaolei] = big_name
    DATA.append(category_IDS)
    DATA.append(BIG_LIST)
    DATA.append(zidian)
    DATA.append(supplier)

def data_collection():
    dangqian_path = os.path.abspath('.')
    com_id = str(DATA[3])
    print("---------------------------")
    print("请输入你要保存的文件名字")
    name = input()
    print("---------------------------")
    file_name = name
    os.mkdir(dangqian_path + "\\" + name)
    name = name + ".csv"
    count = 0
    font_page_data = []
    for i in range(1, 26):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Content-Type": "application/json"
            }
        payload_suoyou = {"brandIds": [], "brandName": "", "casNo": "", "city": "", "orgId": "", "pageSize": 20,
                          "pageNo": i, "sort": 1, "key": "", "maxPrice": "", "minPrice": "", "categoryIds": [],
                          "searchFlag": 11, "supplierIds": [com_id], "supplierName": "", "flag": 10}
        url = "https://www.rjmart.cn/gaea/search"
        web = requests.post(url, headers=headers, data=json.dumps(payload_suoyou))
        data_json = json.loads(web.text)
        data_all = data_json.get("data").get("products")
        if font_page_data == data_all:
            print("全部数据大类页面录入完毕")
            print("---------------------------")
            break
        font_page_data = data_all

        with open(name, "a", newline="", encoding="utf-8") as q:
            fieldnames = list(set(data_all[0]))
            writer = csv.DictWriter(q, fieldnames=fieldnames)
            if count == 0:
                writer.writeheader()
                writer.writerows(data_all)
                count += 1
            else:
                writer.writerows(data_all)
                count += 1
        print("\n当前录入全部类别的数据为第{}页".format(count))
        time.sleep(1)
    print("\n开始录入类别数据")
    jincheng = 1
    for j in list(DATA[0].keys()):
        page = 1
        total_page = 1
        try:
            while page <= total_page:
                payload_cateid = {"brandIds": [], "brandName": "", "casNo": "", "city": "", "orgId": "", "pageSize": 20,
                                  "pageNo": page, "sort": 1, "key": "", "maxPrice": "", "minPrice": "",
                                  "categoryIds": [j], "searchFlag": 11, "supplierIds": [com_id], "supplierName": "",
                                  "flag": 10}
                web_id = requests.post(url, headers=headers, data=json.dumps(payload_cateid))
                data_json_id = json.loads(web_id.text)  #
                data_id = data_json_id.get("data").get("products")
                if data_id == []:
                    break
                with open(name, "a", newline="", encoding="utf-8") as n:
                    fieldnames = list(set(data_id[0]))
                    writer = csv.DictWriter(n, fieldnames=fieldnames)
                    writer.writerows(data_id)
                time.sleep(2)  #
                total = data_json_id.get("total")
                if total < 20:
                    total_page = 1
                else:
                    total_page = math.ceil(total / 20)
                print("\r\n当前录入数据类别为{},当前类别进度{}/{}。总进度{}/{}".format(DATA[0][j], page, total_page, jincheng,len(list(DATA[0].keys()))), end="")
                page += 1
        except:
            lose_page[j] = page
            print("\n当前录入失败数据为类别{}的第{}页".format(DATA[0][j], page))
        jincheng += 1
    DATA.append(name)
    DATA.append(file_name)

def data_processing():
    df = pd.read_csv(DATA[4])
    z = df[["categoryId", "name", "brandName", "specification", "productNum", "price"]]
    z = z.drop_duplicates()
    z_types = {"categoryId": str}
    z = z.astype(z_types)
    z = z.replace(DATA[2])
    ex_path = "./" + DATA[5] + "/result.xlsx"
    z.to_excel(ex_path, index=False)  #
    dalei_name = z["categoryId"].unique()
    for i in dalei_name:
        data_z = z[z["categoryId"] == i]
        q = i.replace("/", "_").strip()
        path = "./" + DATA[5] + "/" + q + ".xlsx"
        data_z.to_excel(path, index=False)
    print("\n---------------------------")
    print("写入完成")

def main():
    category_collection()
    data_collection()
    data_processing()

# DATA第0个是公司的所有类别，
# 第1个大类列表，
# 第2个是该公司所有类的大类归属字典，
# 第3个是供应商编号，
# 第4个是保存的文件名,
# 第5个是保存的文件夹名
lose_page = {}
spyder()
DATA = []
main()
if lose_page:
    print("\n错误内容如下")
    print(lose_page)
else:
    print("\n无任何错误")
print("\n爬虫结束")
