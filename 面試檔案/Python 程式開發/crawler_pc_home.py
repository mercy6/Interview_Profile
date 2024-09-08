import requests
import json
import pandas as pd
from itertools import islice
import re

def get_pchome_popular():
    url = 'https://ecapi-cdn.pchome.com.tw/fsapi/ecshop/composition/web/index/v1/data'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    data = json.loads(r.text)

    hot_data = data['hot']['Blocks']
    url_base = 'https://24h.pchome.com.tw/prod/'
    url_img = 'https://img.pchome.com.tw/cs'

    # 創建一個空的 DataFrame
    popular_buy_pchome = pd.DataFrame()

    for block in islice(hot_data, 6):
        node = block['Nodes'][0]# 取得第一個 node

        # 將 node 的資訊添加到 DataFrame
        row = pd.DataFrame({
            'c_pid': [str(node['Link']['Url'])],  # 商品編號
            'prd': [str(node['Link']['Text'])],  # 商品名稱
            'price': [str(node['Link']['Text1'])],  # 商品價格
            'url': [url_base + str(node['Link']['Url'])],  # 商品網址
            'img': [url_img + str(node['Img']['Src'])], # 商品圖片
            })

        popular_buy_pchome = pd.concat([popular_buy_pchome, row], ignore_index = True)

    return popular_buy_pchome

popular = get_pchome_popular()
print(popular)


def get_pchome_restock():
    url = 'https://ecapi-cdn.pchome.com.tw/ecshop/prodapi/v2/replenish/prod&_callback=jsonpcb_replenish&4745771?limit=14&_callback=jsonpcb_replenish'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    
    try:
        r = requests.get(url, headers=headers)
    except:
        print("No items found in API response.")
        return pd.DataFrame()

    try:
        # 使用正規表達式提取 JSON 數據
        match = re.search(r'jsonpcb_replenish\((.*?)\);', r.text, re.DOTALL)
        # 'search' 尋找要的資料
        # (.*?)：非貪婪
        # 're.DOTALL'：任何字母皆會顯示
        
        json_data = match.group(1)
        # 'match.group(1)'：合併相同資料
        data = json.loads(json_data)
        # 解析 JSON 數據
        # 將已編碼的 JSON 字符串 解碼為 Python 對象
        
        restock_data = data if isinstance(data, list) else data.get('Data', [])
        # 檢查data是不是列表
        # 如果不是 就嘗試從 data 字典中取得'Data'對應的值 沒有的話為空列表 []
        # isinstance 判斷對象是否是已知類型

    except:
        print("No data found in match.")
        return pd.DataFrame()
    
    try:
        url_base = 'https://24h.pchome.com.tw/prod/'
        url_img = 'https://img.pchome.com.tw/cs'
        restock_pchome = pd.DataFrame()  

        for item in restock_data:
            row = pd.DataFrame({
                'c_pid': [str(item['Id'])],  # 商品編號
                'prd': [str(item['Name'])],  # 商品名稱
                'price': [float(item.get('Price', {}).get('P', 0))],  # 商品價格
                'url': [url_base + str(item['Id'])],  # 商品網址
                'img': [url_img + str(item['Pic']['S'])],  # 商品圖片
                })

            restock_pchome = pd.concat([restock_pchome, row], ignore_index=True)
    
    except:
        print("DataFrame is wrong.")
        return pd.DataFrame()

    return restock_pchome

restock = get_pchome_restock()
print(restock)

