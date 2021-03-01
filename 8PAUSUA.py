import psutil
import time
import signal
import sys


def handler(sig_num, frame):
    # Gertaera kudeatu
    print('\nSignal handler called with signal ' + str(sig_num))
    print('Check signal number on '
          'https://en.wikipedia.org/wiki/Signal_%28IPC%29#Default_action')
    print('\nExiting gracefully')
    sys.exit(0)


def cpu_ram():
    while True:
        # KODEA: psutil liburutegia erabiliz, %CPU eta %RAM atera
        cpu = kalkulatu_cpu()
        ram = kalkulatu_ram()
        print("CPU: %" + str(cpu) + "\tRAM: %" + str(ram))
        time.sleep(15)


def kalkulatu_cpu():
    return psutil.cpu_percent(interval=1)


def kalkulatu_ram():
    for izena in psutil.virtual_memory()._fields:
        balioa = getattr(psutil.virtual_memory(), izena)
        if izena == 'percent':
            return balioa


if __name__ == "__main__":
    # SIGINT jasotzen denean, "handler" metodoa exekutatuko da
    signal.signal(signal.SIGINT, handler)
    print('Running. Press CTRL-C to exit.')
    cpu_ram()
    while True:
        pass # Ezer ez egin