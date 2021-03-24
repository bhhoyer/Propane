#!usr/bin/env python

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import RPi.GPIO
import datetime

# Build and Send Email
def Send_Email():

	from_addr = "pi email address" #credentials in ignore file
	GMAIL_PASSWORD = "password123" #credentials in ignore file
	to_addr = ["my email address"] #credentials in ignore file
	msg = MIMEMultipart()
	msg['From'] = from_addr
	msg['To'] = ", ".join(to_addr) # .join function used to concatenate email addresses with comma.
	msg['Subject'] = "Propane Alert"

	body = ("Hi,\n\nThis is your house propane tank. You should know that your "
	"propane tank is getting low. Please schedule a refill as soon as possible."
	"\n\n Regards,\nYour PropanePi")

	msg.attach(MIMEText(body, 'plain'))
	text = msg.as_string()
	
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo() #Send mandatory 'hello' to SMTP server
	server.starttls() #Start TLS Encryption
	server.login(from_addr, GMAIL_PASSWORD)
	server.sendmail(from_addr, to_addr, text)
	server.quit()
		
	return
    
# Setup Raspberry Pi GPIO
GPIO_Pin = 18 #GPIO 24
RPi.GPIO.setmode(RPi.GPIO.BOARD) #GPIO's are numbered based on header pin location
RPi.GPIO.setup(GPIO_Pin, RPi.GPIO.IN) #1kohm pull-down resistor installed on board

now = datetime.datetime.now()

log_file = open("/home/pi/Desktop/PropanePi_log", "a")
log_file.write(now.strftime('%Y-%m-%d %H:%M:%S\t'))

if RPi.GPIO.input(GPIO_Pin) == 0:
    log_file.write("Propane Low!\n")
    Send_Email()

if RPi.GPIO.input(GPIO_Pin) == 1:
    log_file.write("Propane Good\n")    
    
log_file.close()    


			
		
