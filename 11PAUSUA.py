import requests
import urllib


metodoa = 'POST'
uria = "https://api.thingspeak.com/channels.json"
goiburuak = {'Host': 'api.thingspeak.com',
             'Content-Type': 'application/x-www-form-urlencoded'}
edukia = {'api_key': 'DY1W1KB7UY8HNVVM',
          'name': 'Nire kanala',
          'field1': "%CPU",
          'field2': "%RAM"}
edukia_encoded = urllib.parse.urlencode(edukia)
goiburuak['Content-Length'] = str(len(edukia_encoded))
erantzuna = requests.request(metodoa, uria, data=edukia_encoded,
                             headers=goiburuak, allow_redirects=False)


kodea = erantzuna.status_code
deskribapena = erantzuna.reason
print(str(kodea) + " " + deskribapena)
edukia = erantzuna.content
print(edukia)