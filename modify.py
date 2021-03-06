# encoding:utf-8
import datetime 
import json

class DataModify():
    mark_list = {'normal', 'nodemcu', 'micropython', 'micropython_ssd1351'}
    def __init__(self):
        with open('sim_15x16.json', 'r') as f:
            self.char_map = json.loads(f.read())
        self.error_dotmatrix = ""

    def weather(self, weather_data, mark='normal'):
        modify_weather = {}
        if mark.lower() not in self.mark_list:
            return {"error":"parameter error"}
        if weather_data.get("code", "") != "ok":
            return {"error":"weather data erroe"}
        modify_weather["code"] = 'ok'
        modify_weather["city"] = weather_data["city"]
        modify_weather["data"] = {}
        if mark == "micropython_ssd1351":
            year = datetime.datetime.now().year
            for day in range(4):
                modify_weather["data"][str(day)] = {}
                modify_weather["data"][str(day)]["weather"] = self.char_dotmatrix(
                                        weather_data["data"][str(day)]["weather"])
                modify_weather["data"][str(day)]["temp"] = self.char_dotmatrix(
                                        weather_data["data"][str(day)]["temp"].replace(' ', '℃'))
                modify_weather["data"][str(day)]["aqi"] = self.char_dotmatrix(
                                        weather_data["data"][str(day)]["aqi"])
                modify_weather["data"][str(day)]["date"] = self.char_dotmatrix(
                                        weather_data["data"][str(day)]["date"].replace("月","/").replace("日",""))
                modify_weather["data"][str(day)]["weather_code"] = weather_data["data"][str(day)]["icon"].split('/')[-1].split('.')[0]
                if day == 0:
                    modify_weather["data"][str(day)]["current_temp"] = self.char_dotmatrix(
                                        weather_data["data"][str(day)]["current_temp"])
                    modify_weather["data"][str(day)]["current_weather"] = self.char_dotmatrix(
                                        weather_data["data"][str(day)]["current_weather"].replace('(实时)', ''))
                    modify_weather["data"][str(day)]["aqi"] = self.char_dotmatrix("空气质量:{}".format(
                                        weather_data["data"][str(day)]["aqi"].replace(",", " ")))
                    modify_weather["data"][str(day)]["date"] = self.char_dotmatrix("{}/{}".format(year, 
                                        weather_data["data"][str(day)]["date"][:9].replace("月","/").replace("日","").strip()))
            return modify_weather
        else:
            return weather_data

    def char_dotmatrix(self, chars):
        dotmatrix_list = []
        if isinstance(chars, list):
            for char in chars:
                char_dotmatrix_list = []
                for c in char:
                    dotmatrix = self.char_map.get(str(ord(c)), '')
                    if dotmatrix:
                        char_dotmatrix_list.append(dotmatrix) 
                    else:
                        char_dotmatrix_list.append(self.error_dotmatrix) 
                dotmatrix_list.append(char_dotmatrix_list)
        elif isinstance(chars, str):
            for c in chars:
                dotmatrix = self.char_map.get(str(ord(c)), '')
                if dotmatrix:
                    dotmatrix_list.append(dotmatrix) 
                else:
                    dotmatrix_list.append(self.error_dotmatrix) 
        return dotmatrix_list 

weather_modify = DataModify()

if __name__ == "__main__":
    from searchweather import Weather
    weather = Weather()
    weather_data = weather.weather_data("成都")
    print(weather_data)
    print(weather_modify.weather(weather_data, "micropython_ssd1351"))
# del DataModify 
