import requests
from bs4 import BeautifulSoup
import os
import json
import sys
from rgbprint import gradient_print
from rgbprint import Color

def findStuff(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    rm = soup.find('div', {'id': 'directory-tree'})
    rm.extract()
    pdf_found = 0
    
    for nav in soup.find_all('nav'):
        nav.extract()
    
    for links in soup.find_all('div'):
        try:
            tlink = link
            tdir = main_path
            data = json.loads(links.get('phx-click'))
            folder = data[0][1]['value']['value'].split('/')[-2].replace(' ', '_')
            tdir += f"/{folder}"
            gradient_print(tdir, start_color="#3498db", end_color="#e74c3c")
            tlink += f"/{folder}"
            gradient_print(tlink, start_color="#3498db", end_color="#e74c3c")
            findStuff(tlink)
            os.system(f"mkdir {tdir}")
            os.chdir(tdir)
        except Exception as e:
            pass
    
    for file in soup.find_all('a'):
        href = file.get('href')
        if href.endswith('.pdf'):
            pdf_found += 1
            name = href.split('/')[-1]
            gradient_print(f"[*] Found: {name}", start_color="#3498db", end_color="#e74c3c")
            resp = requests.get(href)
            with open(f"{tdir}/{name}", 'wb') as fl:
                fl.write(resp.content)
            gradient_print(f"[+] #{pdf_found} Added: {tdir}/{name} ")


if len(sys.argv) < 2:
    print("[!] Incorrect usage:\n %s <link> <destination>" % sys.argv[0])
    sys.exit()

link = sys.argv[1]
main_path = sys.argv[2]
findStuff(link)
