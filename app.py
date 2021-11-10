#from types import resolve_bases
from flask import Flask,request,make_response
import os,json
import pyowm #Python open weather mappyth
from flask_cors import cross_origin,CORS

app=Flask(__name__)
owmapikey='ebdbb7586bf75909c04657a498a07f79'
owm=pyowm.OWM(owmapikey)#Key generated from open weather map


@app.route('/webhook',methods=['POST']) 
@cross_origin()
def webhook():
    req=request.get_json(silent=True,force=True)

    print(req)
    print('Request:')
    print(json.dumps(req))

    res=processRequest(req)
    
    res=json.dumps(res)
    print(res)
    r=make_response(res)
    r.headers['Content-Type']='application/json'
    return r

def processRequest(req):
    
    result=req.get('queryResult')
    parameters=result.get('parameters')
    city=parameters.get('city_names')
    observation=owm.weather_at_place(str(city))
    w=observation.get_weather()
    latlon_res= observation.get_location()
    lat=str(latlon_res.get_lat())
    lon=str(latlon_res.get_lon())


    wind_res=w.get_wind()
    wind_speed=str(wind_res.get('speed'))

    humidity=str(w.get_humidity())

    celsius_result=w.get_temperature('celsius')
    temp_min_celsius=str(celsius_result.get('temp_min'))
    temp_max_celsius=str(celsius_result.get('temp_max'))

    speech="Today the weather in " + str(city) + "is :\n" + "humidity:" + str(humidity) + "\n WindSpeed" + str(wind_speed) + "\n Temperature is :" + str(celsius_result)                         

    return {
        'fulfillmentText':speech,
        'displayText':speech
    }

if __name__=='__main__':
    app.run(debug=True)