from flask import Flask, request, render_template, jsonify, send_from_directory
import requests
from urllib.parse import unquote
from datetime import datetime

app = Flask(__name__)

def get_aqi(city):
    base_url = "https://api.weatherbit.io/v2.0/forecast/airquality"
    api_key = "21e152f862684d209d90a27afd293dfe"  # Replace with your actual Weatherbit API key
    params = {"city": city, "key": api_key}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
        data = response.json()

        if "data" in data and data["data"]:
            aqi_data = data["data"][0]
            aqi = aqi_data.get("aqi")
            pm25 = aqi_data.get("pm25", "N/A")
            pm10 = aqi_data.get("pm10", "N/A")
            o3 = aqi_data.get("o3", "N/A")
            so2 = aqi_data.get("so2", "N/A")
            no2 = aqi_data.get("no2", "N/A")
            co = aqi_data.get("co", "N/A")

            if aqi is not None:
                if 0 <= aqi <= 50:
                    aqic = 'good'
                elif 50 < aqi <= 100:
                    aqic = 'moderate'
                elif 100 < aqi <= 150:
                    aqic = 'unhealthy-sensitive'
                elif 150 < aqi <= 200:
                    aqic = 'unhealthy'
                elif 200 < aqi <= 300:
                    aqic = 'very-unhealthy'
                else:
                    aqic = 'hazardous'

                result = f"AQI in {city}: {aqi} ({aqic}), PM2.5: {pm25}, PM10: {pm10}, O3: {o3}, SO2: {so2}, NO2: {no2}, CO: {co}"

                return result
            else:
                return f"City not found: {city}"
        else:
            return f"City not found: {city}"

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def get_aqi_by_coordinates(latitude, longitude):
    base_url = "https://api.weatherbit.io/v2.0/forecast/airquality"
    api_key = "21e152f862684d209d90a27afd293dfe"  # Replace with your actual Weatherbit API key
    params = {"lat": latitude, "lon": longitude, "key": api_key}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
        data = response.json()

        if "data" in data and data["data"]:
            city = data["city_name"]
            aqi_data = data["data"][0]
            aqi = aqi_data.get("aqi")
            pm25 = aqi_data.get("pm25", "N/A")
            pm10 = aqi_data.get("pm10", "N/A")
            o3 = aqi_data.get("o3", "N/A")
            so2 = aqi_data.get("so2", "N/A")
            no2 = aqi_data.get("no2", "N/A")
            co = aqi_data.get("co", "N/A")

            if aqi is not None:
                if 0 <= aqi <= 50:
                    aqic = 'good'
                elif 50 < aqi <= 100:
                    aqic = 'moderate'
                elif 100 < aqi <= 150:
                    aqic = 'unhealthy-sensitive'
                elif 150 < aqi <= 200:
                    aqic = 'unhealthy'
                elif 200 < aqi <= 300:
                    aqic = 'very-unhealthy'
                else:
                    aqic = 'hazardous'

                result = f"AQI at {city}: {aqi} ({aqic}), PM2.5: {pm25}, PM10: {pm10}, O3: {o3}, SO2: {so2}, NO2: {no2}, CO: {co}"

                return result
            else:
                return f"Invalid coordinates: ({latitude}, {longitude})"
        else:
            return f"Invalid coordinates: ({latitude}, {longitude})"

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Rest of your code remains unchanged

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_aqi', methods=['GET'])
def api_get_aqi():
    city = request.args.get('city')
    latitude = request.args.get('lat')
    longitude = request.args.get('lng')

    if city:
        result = get_aqi(city.lower())
    elif latitude and longitude:
        latitude = unquote(latitude)
        longitude = unquote(longitude)
        result = get_aqi_by_coordinates(latitude, longitude)
    else:
        result = "Invalid request. Provide either city or coordinates."

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)