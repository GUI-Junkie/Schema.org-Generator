from time import sleep
from urllib.error import URLError
from urllib.request import urlopen

i = 0
i_found = 0
while i < 100:
    i += 1
    try:
        with urlopen("http://schema.org/docs/releases.html") as f:
            txt = f.read(5)
        if 31 == txt[0]:  # If the txt is compressed, decompress
            i_found += 1
    except URLError:
        print('URLError')

    sleep(0.1)

print(i_found)

from socket import gethostbyname_ex, gaierror, getaddrinfo


def get_ips_for_host(host):
    try:
        ips = gethostbyname_ex(host)
        print(ips)
    except gaierror:
        print('Error')

# get_ips_for_host('schema.org')

print(getaddrinfo('schema.org', 80))