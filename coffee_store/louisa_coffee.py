"""
Crawler: Louisa Cafe, 路易莎咖啡門市
author: Cavalon Huang
Date: 2021/0714
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup


def louisa_store_crawler(output_file):
    url = 'https://www.louisacoffee.co/visit_result'
    headers = {
        'user-agent': 'Googlebot',
        'Referer': 'https://www.louisacoffee.co/visit',
        'cookies': "_ga=GA1.2.1791132027.1626140926; _gid=GA1.2.346364183.1626243381; laravel_session=eyJpdiI6IllpMU95Szd2NWVyTnRtRFU2eTZZSEE9PSIsInZhbHVlIjoieHhjZ2FVUEhjVVwvVHlIdnUxcXdyK3c4RUUwUTVYWUd0cnFpa0ZXY0dwcTBERGUrYkVsRExxaWFGYnQ5dFpmN0dra091KzBJcDlQVHJrZ2kxdW50cDNBPT0iLCJtYWMiOiJjN2UwY2QyZWU3Y2Y3OWJlYTlkOTYxN2Y4MTcyNjFmZWIxNTg1OGRhMWI3OTUxNzQ5MTQzYTk1MzlhOWI1MzBiIn0%3D"
    }
    # # res = requests.get(url=url, headers=headers)
    data = {"data[country]": "高雄市"}  # 隨便帶資料(ex:澎湖縣、高雄市)都可以得到所有分店資訊
    res = requests.post(url=url, headers=headers, data=data, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    store_information = soup.select('div[class="col-md-6 store_info"]')
    data_list = []
    for item in store_information:
        store_name = item.find("h4")
        store_address = item.find_all("p")
        data_information = [store_name.text,
                            store_address[1].text.split("/")[-1].replace(" ", "")]
        print(data_information)
        data_list.append(data_information)


    # write to excel
    data_columns = pd.DataFrame(data_list, columns=["store", "address"])
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    data_columns.to_excel(writer, sheet_name='geo_location')
    workbook = writer.book
    worksheet = writer.sheets['geo_location']
    writer.save()
    return len(data_list)


if __name__ == "__main__":
    output_file = "./LouisaCoffee_address.xlsx"
    store_amount = louisa_store_crawler(output_file)
    print("Store Amount:", store_amount)
