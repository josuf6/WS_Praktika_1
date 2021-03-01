import requests
import urllib
import time


if __name__ == "__main__":
    while True:
        metodoa = 'POST'
        uria = "https://api.thingspeak.com/update.json"
        goiburuak = {'Host': 'api.thingspeak.com',
                     'Content-Type': 'application/x-www-form-urlencoded'}
        edukia = {'api_key': 'KI91D7MI21FRWH4T',
                  'field1': "8",
                  'field2': "10"}
        edukia_encoded = urllib.parse.urlencode(edukia)
        goiburuak['Content-Length'] = str(len(edukia_encoded))
        erantzuna = requests.request(metodoa, uria, data=edukia_encoded,
                                     headers=goiburuak, allow_redirects=False)

        kodea = erantzuna.status_code
        deskribapena = erantzuna.reason
        print(str(kodea) + " " + deskribapena)
        edukia = erantzuna.content
        print(edukia)

        time.sleep(15)