# 這檔案是抓取氣象平台 API 所有縣市的 36 小時資料

import requests
# 匯入 requests 模組

def get_data():
# 定義一個函數 get_data    
    
    url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001'
    # 設定抓取 API 的 URL
    
    headers = {
        'Authorization': 'CWA-F14FD326-2563-4B88-8D66-79DE28E54653',
    }
    # 設定標頭，識別身份授權碼
    
    response = requests.get(url, headers=headers)
    # 用get獲取url資源

    if response.status_code == 200:
    # 檢查狀態碼是否為 200 
        
        response_json = response.json()
        # 將回應的 json 資料轉換成 python 字典
        
        locations = response_json["records"]["location"]
        # 從字典中取出需求範圍需要的資料
        
        for location in locations:
            # 迴圈處理每個縣市的資料
            city_name = location["locationName"]
            # 抓取縣市資料
            weather_description = location["weatherElement"][0]["time"][0]["parameter"]["parameterName"]
            # 抓取天氣現象資料
            PoP_description = location["weatherElement"][1]["time"][0]["parameter"]["parameterName"]
            # 抓取降雨機率資料
            MinT_description = location["weatherElement"][2]["time"][0]["parameter"]["parameterName"]
            # 抓取溫度資料
            MaxT_description = location["weatherElement"][4]["time"][0]["parameter"]["parameterName"]
            # 抓取最高溫度資料
            CI_description = location["weatherElement"][3]["time"][0]["parameter"]["parameterName"]
            #抓取舒適度資料
            
            print(f"地區: {city_name}")
            print(f"天氣現象: {weather_description}")
            print(f"降雨機率: {PoP_description}％")
            print(f"溫度: {MinT_description}～{MaxT_description}°C")
            print(f"最高溫度: {MaxT_description}°C")
            print(f"舒適度: {CI_description}")
            print("-----------------------------")
            # 顯示所有天氣資訊
    else:
        
        print("抓取不到資料")
        # 若狀態碼不是 200，顯示錯誤訊息
get_data()
# 呼叫 get_data 函數，執行爬蟲
