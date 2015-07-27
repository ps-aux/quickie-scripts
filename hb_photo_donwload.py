#!/usr/bin/env python

import sys
import os
import requests
import bs4

check_url = 'www.horskybeh.sk'


def usage():
    script_name = os.path.basename(sys.argv[0])
    print("Usage: {} <web page url> <output directory>".format(script_name))


if len(sys.argv) != 3:
    usage()
    sys.exit(1)

url = sys.argv[1]
path = sys.argv[2]

if check_url not in url:
    print('Warning: Seems that specified URL does is not ', check_url,
          '\nThe script might not work')

split_url = url.split('/')
split_url = split_url[:-1]

root_url = '/'.join(split_url) + '/'

response = requests.get(url)

soup = bs4.BeautifulSoup(response.text, 'html.parser')

slide_show_no = 1
img_links = []

# Loop through all SlideShowN elements and collect <a> elements
# with image urls
while True:
    div = soup.find(id='SlideShow{}'.format(slide_show_no))
    slide_show_no += 1
    if div is None:
        break
    img_links += div.find_all('a')


# Append trailing slash if necessary
if not path[-1] == os.sep:
    path += os.sep

# Create dir if does not exist
if not os.path.exists(path):
    os.makedirs(path)

print("Will download images from {} links".format(len(img_links)))
# Image number counter
i = 0
for a in img_links:
    img_url = root_url + a['href']
    img_name = img_url.split('/')[-1]
    img_path = path + img_name
    print("Downloading " + img_url)
    response = requests.get(img_url)
    f = open(img_path, 'wb')
    print('Saving image ' + img_path)
    f.write(response.content)
    f.close()
    i += 1

print("Finished: {} images saved".format(i))
