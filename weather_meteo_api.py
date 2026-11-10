import requests

def cal(temp,rain):
    if temp < 5:
        temp_status = 'Cold'
    elif temp >= 5 and temp <25:
        temp_status = 'Mild'
    else:
        temp_status = 'Hot'

    if rain > 0:
        rain_status = 'Rain'
    else:
        rain_status = 'No Rain'
    return temp_status,rain_status


cities = {'Los Angeles':(34.0522,-118.2437),'New York':(40.7128,-74.0060),'Paris':(48.8566,2.3522),'Munich':(48.1372,11.5761),'Istanbul':(41.0082,28.9784),'Dubai':(25.2048,55.2708),'Bangkok':(13.7563,100.5018),'Shanghai':(31.2304,121.4737),'Tokyo':(35.6762,139.6503),'Sydney':(-33.8688,151.2093)}

for city in cities:

    latitude,longitude = cities [city]

    weather_url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min&current=temperature_2m,rain,wind_speed_10m&timezone=Europe%2FBerlin&forecast_days=14'

    responds = requests.get(weather_url,timeout = 15)

    weather_data = responds.json()

    weather_observation = [{'City':city, 'Temperature Cel': weather_data['current']['temperature_2m'],'Wind speed kmh':weather_data['current']['wind_speed_10m'],'Rain mm':weather_data['current']['rain'],'Observation Time':weather_data['current']['time']}]

    forecast_dates = weather_data['daily']['time']

    forecast_max_temps = weather_data['daily']['temperature_2m_max']

    forecast_min_temps = weather_data['daily']['temperature_2m_min']

    weather_forecast_report = []


    for weather in weather_observation:

        temp_status,rain_status = cal (weather['Temperature Cel'],weather['Rain mm'])

        if weather['Temperature Cel'] >= -50 and weather['Temperature Cel'] <= 60:
            validation_temp_status = ('Temperature Range OK')
        else:
            validation_temp_status  = ('Temperature out of Range')

        if weather['Wind speed kmh'] >= 0:
            validation_wind_status = ('Wind speed Range OK')
        else:
            validation_wind_status = ('Wind out of Range')

        if weather['Rain mm'] >= 0:
            validation_rain_status = ('Rain Range OK ')
        else:
            validation_rain_status = ('Rain out of Range')

        print('\nCity:',weather['City'],'\nTime:',weather['Observation Time'], '\nTemperature:',weather['Temperature Cel'],'\t',validation_temp_status ,'\nWind:',weather['Wind speed kmh'],'\t',validation_wind_status, '\nRain:',weather['Rain mm'],'\t',validation_rain_status, '\nTemperature Status:',temp_status,'\nRain Status:', rain_status)



    for date,temp_max,temp_min in zip(forecast_dates,forecast_max_temps,forecast_min_temps):

        forecast_day = {'Date': date,'Maximum Temperature': temp_max,'Minimum Temperature': temp_min}

        weather_forecast_report.append(forecast_day)

        print ('Date:',date, '\tMax Temperature:', temp_max, '°C' ' \tMin Temperature:',temp_min, '°C')

    print('\nWEATHER REPORT')

    print(weather_forecast_report)

    weather_webhook = 'https://n8n.nextlablogic.com/webhook/23cc0824-144d-45ce-a3c9-15f3bf6f8e34'

    responds = requests.post(weather_webhook,json = weather_observation + weather_forecast_report)




