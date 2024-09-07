import requests
import pandas as pd

'''
說明:抓取天氣api資料 查詢縣市天氣資訊
search_county:輸入想查詢的縣市 ex:'臺北市' '全部縣市'
search_time:輸入想查詢的時段 0:全部時段 1:最近的12小時時段 2:下一個12小時時段 3:下下個12小時時段
'''


def get_weather(search_county, search_time):
    authorization = "CWA-441C96CF-64CA-49A9-A924-4A2268C0A6A1"
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization="
    url = url + authorization

    data = requests.get(url)  # 取得 JSON 檔案的內容為文字
    data_json = data.json()  # 轉換成 JSON 格式
    weather_df = pd.DataFrame(columns=['county', 'start_time', 'end_time', 'wx', 'pop', 'minT', 'ci', 'maxT'])

    # 迭代 records 字典，找到指定縣市的天氣資訊 遍歷 records 字典中的 location 列表(22個縣遍歷22次)
    for location_info in data_json['records']['location']:
        county = location_info['locationName']
        weather_elements = location_info['weatherElement']

        for i in range(len(weather_elements[0]['time'])):
            #i控制各個時間段，舉例 i=0:最近12小時區段，以此類推
            data_to_append = {
                'county': county,                                                       #縣市
                'start_time': weather_elements[0]["time"][i]["startTime"],              #起始時間，取weatherElement下Wx的時間
                'end_time': weather_elements[0]["time"][i]["endTime"],                  #結束時間，取weatherElement下Wx的時間
                'wx': weather_elements[0]["time"][i]["parameter"]["parameterName"],     #天氣狀態，取weatherElement下Wx
                'pop': weather_elements[1]["time"][i]["parameter"]["parameterName"]+'%',    #降雨機率，取weatherElement下Pop
                'minT': weather_elements[2]["time"][i]["parameter"]["parameterName"]+chr(176),   #最低溫度，取weatherElement下MinT
                'ci': weather_elements[3]["time"][i]["parameter"]["parameterName"],     #舒適度，取weatherElement下CI
                'maxT': weather_elements[4]["time"][i]["parameter"]["parameterName"]+chr(176)    #最高溫度，取weatherElement下MaxT
            }
            weather_df = weather_df._append(data_to_append, ignore_index=True)
    # 如果 search_county 是 "全部縣市"，則將 target_df 設置為整個 DataFrame
    if search_county == '全部縣市':
        target_df = weather_df
    else:
        target_df = weather_df[weather_df['county'] == search_county]

    # 根據 search_time 返回 county 的指定時間資料
    if search_time == 0:
        target_df = target_df

    elif search_time in [1, 2, 3]:
        target_df = target_df.groupby('county').nth(search_time - 1)    #按照county的值進行分組，nth()選取指定row的資料

    return target_df



# 使用範例
s1 = get_weather('臺北市', 1)
s0 = get_weather('臺北市', 0)
print(s1)
print(s0)
# 使用全部縣市
all_counties2 = get_weather('全部縣市', 2)
all_counties0 = get_weather('全部縣市', 0)
print(all_counties2)
print(all_counties0)