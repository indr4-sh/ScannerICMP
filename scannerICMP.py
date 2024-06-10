#!/usr/bin/env python3

import argparse
import subprocess
import signal
import sys
from concurrent.futures import ThreadPoolExecutor
def handler(sig, frame):
    print("Saliendo...")
    sys.exit(1)

signal.signal(signal.SIGINT, handler)

def get_arguments():
    parser = argparse.ArgumentParser(description="Herramienta para descubrir host via ICMP")
    parser.add_argument("-t", "--target", required=True, dest="target", help="Host o rango de red a escanear")
    args = parser.parse_args()

    return args.target

def parse_target(target_str):

    target_str_splitted = target_str.split(".")
    first_three_octets = '.'.join(target_str_splitted[:3])

    if len(target_str_splitted) == 4:
        if "-" in target_str_splitted[3]:
            start, end = target_str_splitted[3].split('-')
            return [f"{first_three_octets}.{i}" for i in range(int(start), int(end)+1)]
        else:
            return [target_str]
    else:
        print("El formato de la IP o rango de IP no son correctos")
    
def host_discover(target):
    try:
        ping = subprocess.run(["ping", "-c", "1", target], timeout=1, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if ping.returncode == 0:
            print(f"La ip {target} está abierta")
    except subprocess.TimeoutExpired:
        pass

def main():
    target_str = get_arguments()
    targets = parse_target(target_str)

    print("Host activos:\n")
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(host_discover, targets)

if __name__ == '__main__':
    main()