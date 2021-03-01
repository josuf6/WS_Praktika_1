import signal
import sys
import requests
import urllib
import time
import json


def handler(sig_num, frame):
    # Gertaera kudeatu
    print('\nSignal handler called with signal ' + str(sig_num))
    print('Check signal number on '
          'https://en.wikipedia.org/wiki/Signal_%28IPC%29#Default_action')
    print('\nExiting gracefully')
    sys.exit(0)


def kanala_sortu():
    metodoa = 'POST'
    uria = "https://api.thingspeak.com/channels.json"
    goiburuak = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    edukia = {'api_key': 'DY1W1KB7UY8HNVVM',
              'name': '14PAUSUA',
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
    return json.loads(edukia)


def datuak_bidali(write_api_key):
    while True:
        metodoa = 'POST'
        uria = "https://api.thingspeak.com/update.json"
        goiburuak = {'Host': 'api.thingspeak.com',
                     'Content-Type': 'application/x-www-form-urlencoded'}
        edukia = {'api_key': write_api_key,
                  'field1': "43",
                  'field2': "82"}
        print(edukia)
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


if __name__ == '__main__':
    # SIGINT jasotzen denean, "handler" metodoa exekutatuko da
    signal.signal(signal.SIGINT, handler)
    print('Running. Press CTRL-C to exit.')
    hiztegia = kanala_sortu()
    datuak_bidali(hiztegia["api_keys"][0]["api_key"])