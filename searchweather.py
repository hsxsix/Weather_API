#encoding:utf-8
import datetime
from urllib.parse import quote 

import requests
from lxml import etree as et 

class Weather(): 
    def __init__(self):
        baiduhomepage = "https://www.baidu.com"
        self.url = (baiduhomepage+"/s?ie=utf-8"
                "&f=8"
                "&rsv_bp=0"
                "&rsv_idx=1"
                "&tn=baidu"
                "&wd=%s"
                "&rqlang=cn"
                "&rsv_enter=1"
                "&rsv_sug3=2")
        self.headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Host": "www.baidu.com",
                "Cookie":"BAIDUID=05D73F0269B5857EEBD199CE0F4F9D67:FG=1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.12 Safari/537.36"
                }

    def weather_data(self, keywords):
        kd = (quote(keywords+" 天气",'utf-8'))
        html_code = requests.get(url=self.url % kd, headers=self.headers, timeout=5)
        # print(html_code.text)
        selector = et.HTML(html_code.content, parser=et.HTMLParser(encoding='utf-8'))
        weather_selector = selector.xpath('//div[@id="content_left"]//div[@id="1"]')
        if weather_selector:
            try:
                weather_data = self._parser_weather_data(weather_selector[0], node)
                return weather_data 
            except Exception as e:
                print(e)
                return {"code":"error", "city":keywords, "data":"获取数据失败!Get data failed!"}
        else:
            return {"code":"error", "city":keywords, "data":"获取数据失败!Get data failed!"}
        
    def _parser_weather_data(self, weather_selector, node):
        city = ''.join(weather_selector.xpath('.//h3[@class="t c-gap-bottom-small"]/a//text()'))[:-17]
        today = weather_selector.xpath('.//div[@class="op_weather4_twoicon"]/a[1]')[0]
        today_date = ''.join(today.xpath('./p[@class="op_weather4_twoicon_date"]/text()')).strip() 
        today_icon = ''.join(today.xpath('.//div[@class="op_weather4_twoicon_icon"]/@style')).split(";")[0].split("url(")[1].replace(")",'')
        current_temp = ''.join(today.xpath('.//span[@class="op_weather4_twoicon_shishi_title"]/text()')).strip()  
        current_weather = ''.join(today.xpath('.//span[@class="op_weather4_twoicon_shishi_data"]/i/text()')).strip('℃')
        today_temp = ''.join(today.xpath('.//p[@class="op_weather4_twoicon_temp"]/text()')).strip('℃')
        today_weather = ''.join(today.xpath('.//p[@class="op_weather4_twoicon_weath"]/text()')).strip() #.replace(' ','').replace('\n','')
        today_wind = ''.join(today.xpath('.//p[@class="op_weather4_twoicon_wind"]/text()'))
        today_aqi = ','.join(today.xpath('.//div[@class="op_weather4_twoicon_realtime_quality_wrap"]/span/span/text()')).replace('\n','').replace(' ','')

        tomorrow = weather_selector.xpath('.//div[@class="op_weather4_twoicon"]/a[2]')[0]
        tomorrow_date = ''.join(tomorrow.xpath('.//p[@class="op_weather4_twoicon_date_day"]/text()'))
        tomorrow_week = ''.join(tomorrow.xpath('.//p[@class="op_weather4_twoicon_date"]/text()')).strip() 
        tomorrow_icon = ''.join(tomorrow.xpath('.//div[@class="op_weather4_twoicon_icon"]/@style')).split(";")[0].split("url(")[1].replace(")",'')
        tomorrow_temp = ''.join(tomorrow.xpath('.//p[@class="op_weather4_twoicon_temp"]/text()')).strip().strip('℃')
        tomorrow_weather = ''.join(tomorrow.xpath('.//p[@class="op_weather4_twoicon_weath"]/text()')).strip() 
        tomorrow_wind = ''.join(tomorrow.xpath('.//p[@class="op_weather4_twoicon_wind"]/text()'))
        tomorrow_aqi = ''.join(tomorrow.xpath('.//div[@class="op_weather4_twoicon_realtime_quality_wrap"]/span/text()')).strip() 
        
        acquired = weather_selector.xpath('.//div[@class="op_weather4_twoicon"]/a[3]')[0]
        after_tomorrow_date = ''.join(acquired.xpath('.//p[@class="op_weather4_twoicon_date_day"]/text()'))
        after_tomorrow_week = ''.join(acquired.xpath('.//p[@class="op_weather4_twoicon_date"]/text()')).strip()  
        after_tomorrow_icon = ''.join(acquired.xpath('.//div[@class="op_weather4_twoicon_icon"]/@style')).split(";")[0].split("url(")[1].replace(")",'')
        after_tomorrow_temp = ''.join(acquired.xpath('.//p[@class="op_weather4_twoicon_temp"]/text()')).strip('℃')
        after_tomorrow_weather = ''.join(acquired.xpath('.//p[@class="op_weather4_twoicon_weath"]/text()')).strip()
        after_tomorrow_wind = ''.join(acquired.xpath('.//p[@class="op_weather4_twoicon_wind"]/text()'))
        after_tomorrow_aqi = ''.join(acquired.xpath('.//div[@class="op_weather4_twoicon_realtime_quality_wrap"]/span/text()')).strip() 
        
        three_day = weather_selector.xpath('.//div[@class="op_weather4_twoicon"]/a[4]')[0]
        after_three_day_date = ''.join(three_day.xpath('.//p[@class="op_weather4_twoicon_date_day"]/text()'))
        after_three_day_week = ''.join(three_day.xpath('.//p[@class="op_weather4_twoicon_date"]/text()')).strip() 
        after_three_day_icon = ''.join(three_day.xpath('.//div[@class="op_weather4_twoicon_icon"]/@style')).split(";")[0].split("url(")[1].replace(")",'')
        after_three_day_temp = ''.join(three_day.xpath('.//p[@class="op_weather4_twoicon_temp"]/text()')).strip('℃')
        after_three_day_weather = ''.join(three_day.xpath('.//p[@class="op_weather4_twoicon_weath"]/text()')).strip() 
        after_three_day_wind = ''.join(three_day.xpath('.//p[@class="op_weather4_twoicon_wind"]/text()'))
        after_three_day_aqi = ''.join(three_day.xpath('.//div[@class="op_weather4_twoicon_realtime_quality_wrap"]/span/text()')).strip() 
        
        four_day = weather_selector.xpath('.//div[@class="op_weather4_twoicon"]/a[5]')[0]
        after_four_day_date = ''.join(four_day.xpath('.//p[@class="op_weather4_twoicon_date_day"]/text()'))
        after_four_day_week = ''.join(four_day.xpath('.//p[@class="op_weather4_twoicon_date"]/text()')).strip()
        after_four_day_icon = ''.join(four_day.xpath('.//div[@class="op_weather4_twoicon_icon"]/@style')).split(";")[0].split("url(")[1].replace(")",'')
        after_four_day_temp = ''.join(four_day.xpath('.//p[@class="op_weather4_twoicon_temp"]/text()')).strip('℃')
        after_four_day_weather = ''.join(four_day.xpath('.//p[@class="op_weather4_twoicon_weath"]/text()')).strip() 
        after_four_day_wind = ''.join(four_day.xpath('.//p[@class="op_weather4_twoicon_wind"]/text()'))
        after_four_day_aqi = ''.join(four_day.xpath('.//div[@class="op_weather4_twoicon_realtime_quality_wrap"]/span/text()')).strip() 

        weather_data = {
                "code":"ok",
                "city":city,
                "data":{
                    "0":{
                        "date":today_date,
                        "icon":today_icon,
                        "current_temp":current_temp,
                        "current_weather":current_weather,
                        "temp":today_temp,
                        "weather":today_weather,
                        "wind":today_wind,
                        "aqi":today_aqi 
                        },
                    "1":{
                        "date":tomorrow_date,
                        "icon":tomorrow_icon,
                        "temp":tomorrow_temp,
                        "weather":tomorrow_weather,
                        "wind":tomorrow_wind,
                        "aqi":tomorrow_aqi 
                        },
                    "2":{
                        "date":after_tomorrow_date,
                        "icon":after_tomorrow_icon,
                        "temp":after_tomorrow_temp,
                        "weather":after_tomorrow_weather,
                        "wind":after_tomorrow_wind,
                        "aqi":after_tomorrow_aqi 
                        },
                    "3":{
                        "date":after_three_day_date,
                        "icon":after_three_day_icon,
                        "temp":after_three_day_temp,
                        "weather":after_three_day_weather,
                        "wind":after_three_day_wind,
                        "aqi":after_three_day_aqi 
                        },
                    "4":{
                        "date":after_four_day_date,
                        "icon":after_four_day_icon,
                        "temp":after_four_day_temp,
                        "weather":after_four_day_weather,
                        "wind":after_four_day_wind,
                        "aqi":after_four_day_aqi 
                        }
                    }
                }
        print("get weather data from net")
        return weather_data 

def get_city_by_ip(ip_addr):
    pass
if __name__ == "__main__":
    city = input("请输入城市名:")
    w = GetWeather()
    weather = w.get_weather_data(city, "esp8266")
    print(weather)
