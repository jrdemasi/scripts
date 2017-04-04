#!/usr/bin/env python3

from urllib.request import urlopen
import re
import sys

url = sys.argv[1]

website = urlopen(url)

html = str(website.read())

links = re.findall('"((http|ftp)s?://.*?)"', html)

print(links)
