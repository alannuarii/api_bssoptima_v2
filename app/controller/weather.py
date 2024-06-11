import requests
from bs4 import BeautifulSoup as bs


class Weather:
    url = "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-SulawesiUtara.xml"
    response = requests.get(url, verify=True)
    sangihe = bs(response.text, "xml")

    def get_weather(self):
        cuaca = self.sangihe.find(id="501536").find(id="weather")
        h12 = cuaca.find(h="12").value.string
        result = h12
        return result
