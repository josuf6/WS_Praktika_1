import psutil
import time
import signal
import sys
import requests
import urllib
import json


api_key = 'DY1W1KB7UY8HNVVM'
datuak = []


def handler(sig_num, frame):
    # Erabilitako kanala hustu
    kanala_hustu()

    # Gertaera kudeatu
    print('\nSignal handler called with signal ' + str(sig_num))
    print('Check signal number on '
          'https://en.wikipedia.org/wiki/Signal_%28IPC%29#Default_action')
    print('\nExiting gracefully')
    sys.exit(0)


def kanala_hustu():
    # Eskaera egin
    metodoa = 'DELETE'
    uria = "https://api.thingspeak.com/channels/" + str(datuak[0]) + "/feeds.json"
    goiburuak = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    edukia = {'api_key': api_key}
    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburuak['Content-Length'] = str(len(edukia_encoded))
    erantzuna = requests.request(metodoa, uria, data=edukia_encoded,
                                 headers=goiburuak, allow_redirects=False)

    # Lortutako erantzunari buruzko informazioa pantailaratu
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print(str(kodea) + " " + deskribapena)
    edukia = erantzuna.content
    print(edukia)


def kanala_sortu():
    # Eskaera egin
    metodoa = 'POST'
    uria = "https://api.thingspeak.com/channels.json"
    goiburuak = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    edukia = {'api_key': api_key,
              'name': 'Nire kanala',
              'field1': "%CPU",
              'field2': "%RAM"}
    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburuak['Content-Length'] = str(len(edukia_encoded))
    erantzuna = requests.request(metodoa, uria, data=edukia_encoded,
                                 headers=goiburuak, allow_redirects=False)

    # Lortutako erantzunari buruzko informazioa pantailaratu
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print(str(kodea) + " " + deskribapena)
    edukia = erantzuna.content
    print(str(edukia) + "\n")

    # Kanalaren ID-a eta Write API Key-a erantzunan jasotako JSON objektutik atera
    hiztegia = json.loads(edukia)
    kanala_id = hiztegia["id"]
    write_api_key = hiztegia["api_keys"][0]["api_key"]
    return kanala_id, write_api_key


def datuak_bidali():
    while True:
        # Erabilitako CPU eta RAM balioak kalkulatu
        cpu = kalkulatu_cpu()
        ram = kalkulatu_ram()
        print("CPU: %" + str(cpu) + "\tRAM: %" + str(ram))

        # Eskaera egin
        metodoa = 'POST'
        uria = "https://api.thingspeak.com/update.json"
        goiburuak = {'Host': 'api.thingspeak.com',
                     'Content-Type': 'application/x-www-form-urlencoded'}
        edukia = {'api_key': datuak[1],
                  'field1': cpu,
                  'field2': ram}
        print(edukia)
        edukia_encoded = urllib.parse.urlencode(edukia)
        goiburuak['Content-Length'] = str(len(edukia_encoded))
        erantzuna = requests.request(metodoa, uria, data=edukia_encoded,
                                     headers=goiburuak, allow_redirects=False)

        # Lortutako erantzunari buruzko informazioa pantailaratu
        kodea = erantzuna.status_code
        deskribapena = erantzuna.reason
        print(str(kodea) + " " + deskribapena)
        edukia = erantzuna.content
        print(str(edukia) + "\n")

        # 15 segundoko etenaldia
        time.sleep(15)


def kalkulatu_cpu():
    return psutil.cpu_percent(interval=1)


def kalkulatu_ram():
    for izena in psutil.virtual_memory()._fields:
        balioa = getattr(psutil.virtual_memory(), izena)
        if izena == 'percent':
            return balioa


if __name__ == '__main__':
    # SIGINT jasotzen denean, "handler" metodoa exekutatuko da
    signal.signal(signal.SIGINT, handler)
    print('Running. Press CTRL-C to exit.\n')
    datuak = kanala_sortu()
    datuak_bidali()