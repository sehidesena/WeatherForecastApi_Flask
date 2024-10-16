from flask import Flask, jsonify
import requests

app = Flask(__name__)

API_KEY = "53fba4c3e76f74e161e8c746c00116d9"
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"


@app.route('/forecast/<lat>/<lon>', methods=['GET'])
def get_forecast(lat, lon):
    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return jsonify({"error": "Invalid latitude or longitude"}), 400

    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'en'
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        forecast_data = response.json()


        city_name = forecast_data['city']['name']
        country_code = forecast_data['city']['country']
        temperature = forecast_data['list'][0]['main']['temp']
        description = forecast_data['list'][0]['weather'][0]['description']
        icon = forecast_data['list'][0]['weather'][0]['icon']



        hourly_forecast = [
            {
                "time": forecast['dt_txt'],
                "temperature": forecast['main']['temp'],
                "description": forecast['weather'][0]['description'],
                "icon": forecast['weather'][0]['icon']
            }
            for forecast in forecast_data['list'][:5]
        ]


        daily_forecast = []
        for i in range(0, len(forecast_data['list']), 8):
            day = forecast_data['list'][i]
            daily_forecast.append({
                "date": day['dt_txt'].split(' ')[0],
                "temperature": day['main']['temp'],
                "description": day['weather'][0]['description'],
                "icon": day['weather'][0]['icon']
            })

        result = {
            "currentWeather" :  {
                "city": city_name,
                "country_code": country_code,
                "icon" : icon,
                "temperature" : temperature
            },
            "hourly" : hourly_forecast,
            "daily":daily_forecast,

        }

        return jsonify(result)
    else:
        return jsonify({
            "error": "Failed to retrieve forecast data",
            "status_code": response.status_code,
            "response_text": response.text
        }), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
