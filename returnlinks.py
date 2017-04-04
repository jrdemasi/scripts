#!/usr/bin/env python3

"""
"Crawls" a website and returns all of the links that appear on the site.
Can be modified for other protocols, but the below covers http, https,
and ftp.
"""


from urllib.request import urlopen
import re
import sys

url = sys.argv[1]

website = urlopen(url)

html = str(website.read())

links = re.findall('"((http|ftp)s?://.*?)"', html)

print(links)
