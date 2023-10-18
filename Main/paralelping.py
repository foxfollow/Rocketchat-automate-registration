import subprocess
import concurrent.futures
import sys
import ipaddress

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def ping(host):
    if is_valid_ip(host):
        result = subprocess.run(['ping', '-c', '20', host], stdout=subprocess.PIPE)
        return result.stdout.decode()
    else:
        return f"{host} is not a valid IP address."

def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        hosts = sys.argv[1:]
        results = executor.map(ping, hosts)

        for result in results:
            print(result)

if __name__ == "__main__":
    main()
