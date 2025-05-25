import requests
from bs4 import BeautifulSoup

#
    
    # Tìm các thẻ chứa dữ liệu thời tiết (cần điều chỉnh theo cấu trúc HTML thực tế)
 #
# Sử dụng trong views.py
# forecast = [scrape_weather()]


def scrape_weather():
    url = "https://www.accuweather.com/vi/vn/ho-chi-minh-city/353981/weather-forecast/353981"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    temp = soup.find('div', class_='temp').text.strip()  # Cần kiểm tra class thực tế
    return {'temp': float(temp.replace('°C', '')), 'description': 'mưa nhẹ', 'humidity': 85, 'wind_speed': 3.5, 'rain': 2.5}