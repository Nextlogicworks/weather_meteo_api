import requests
weather_url = 'https://api.open-meteo.com/v1/forecast?latitude=48.137154&longitude=11.576124&daily=temperature_2m_max,temperature_2m_min&current=temperature_2m,rain,wind_speed_10m&timezone=Europe%2FBerlin&forecast_days=14'
responds = requests.get(weather_url)
weather_data = responds.json()
print(weather_data['daily'].keys())


weather_observation = [{'City':'Munich', 'Temperature Cel': weather_data['current']['temperature_2m'],'Wind speed kmh':weather_data['current']['wind_speed_10m'],'Rain mm':weather_data['current']['rain'],'Observation Time':weather_data['current']['time']}]

forecast_dates = weather_data['daily']['time']

forecast_max_temps = weather_data['daily']['temperature_2m_max']

forecast_min_temps = weather_data['daily']['temperature_2m_min']


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

print('\nWEATHER REPORT')

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


weather_forecast_report = []


for date,temp_max,temp_min in zip(forecast_dates,forecast_max_temps,forecast_min_temps):

    forecast_day = {'Date': date,'Maximum Temperature': temp_max,'Minimum Temperature': temp_min}

    weather_forecast_report.append(forecast_day)

    print ('Date:',date, '\tMax Temperature:', temp_max, '°C' ' \tMin Temperature:',temp_min, '°C')


print(weather_forecast_report)

weather_webhook = 'https://sert333.app.n8n.cloud/webhook/23cc0824-144d-45ce-a3c9-15f3bf6f8e34'

responds = requests.post(weather_webhook,json = weather_observation + weather_forecast_report)




