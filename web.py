#coding:utf-8
import sys
sys.path.append('../')

from urllib.parse import urlencode
from flask import Flask, request, jsonify
from flask_caching import Cache
from searchweather import GetWeather
from modify import weather_modify

cache_config = {
        "CACHE_TYPE":"redis",
        "CACHE_REDIS_HOST":"172.27.0.14",
        "CACHE_REDIS_PORT":"12015",
        "CACHE_REDIS_DB":"",
        "CACHE_REDIS_PASSWORD": "sUS7?io#hP%m6ODB"
        }
weather = GetWeather()

app = Flask(__name__)
cache = Cache(app,config=cache_config)

def cache_key():
    args = request.args 
    key = request.path+'?'+urlencode([(k,v.upper()) for k in sorted(args) for v in sorted(args.getlist(k))])
    return key 

@app.route("/weather/v1",methods=['GET'])
@cache.cached(timeout=20*60, key_prefix=cache_key)
def getweather():
    _args = ["city","node"]
    if request.method == "GET":
        ip = request.remote_addr
        # print("ip是{}".format(ip))
        inspect = set(request.args.keys()).issubset(_args)
        city, node = request.args.get('city', ''), request.args.get('node', 'normal')
        weather_data = weather.weather_data(city)
        result_weather = weather_modify.weather(weather_data, node)
        
        return jsonify(result_weather) if inspect else \
                jsonify({"code":"error","data":"参数错误！Parameter error！"})
    return jsonify({"code":"error","data":"错误的请求方式！Request method error！"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8008)
