from flask import Blueprint, send_from_directory, request, jsonify
import uuid
from threading import Thread
import yahoo_fin.stock_info as si
import time
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from twilio.rest import Client
static_folder = 'static'
def index():
    return send_from_directory(static_folder, 'build/index.html')
def serve_js(path):
    return send_from_directory(static_folder, f'build/static/js/{path}')
def serve_css(path):
    return send_from_directory(static_folder, f'build/static/css/{path}')
def serve_media(path):
    return send_from_directory(static_folder, f'build/static/media/{path}')


def send_alert_background_task(alert_id, SymbolName, stockPrice, stockNotificationType, notificationPayload, stockCheckInterval):
    # This function will run in the background
    sendAlert(alert_id, SymbolName, stockPrice, stockNotificationType, notificationPayload, stockCheckInterval)

def stockAlert():
    try:
        data = request.get_json()
        data = dict(data)
        SymbolName=data['symbol']
        stockPrice=data['thresholdPrice']
        stockNotificationType=data['notification']
        notificationPayload=data['payLoad']
        stockCheckInterval=data['frequency']
        # Generate a unique ID for the alert
        alert_id = str(uuid.uuid1())
        # Start a new thread to run sendAlert in the background
        thread = Thread(target=send_alert_background_task, args=(alert_id, SymbolName, stockPrice, stockNotificationType, notificationPayload, stockCheckInterval))
        thread.start()
        return jsonify({'status': 'success', 'message': 'Stock Alert Created', 'alert_id': alert_id})
    
    except Exception as e:
        return jsonify({'status': 'fail', 'message': str(e)})
    


#function to send alert to the user=> main function
def sendAlert(alet_id,SymbolName,MystockPrice,stockNotificationType,notificationPayload,stockCheckInterval):
    currentPrice = si.get_live_price(SymbolName)
    MystockPrice=float(MystockPrice)
    check_thresholdLoop(SymbolName, MystockPrice,stockNotificationType,notificationPayload,stockCheckInterval)
    
#function to manage the loop for checking the stock price
def check_thresholdLoop(SymbolName, MystockPrice,stockNotificationType,notificationPayload,stockCheckInterval):
        if stockCheckInterval=="Daily":
            timer=24*60
        elif stockCheckInterval=="Hourly":
            timer = 60
        else:
            timer = 24*7*60    
        print
            
        while True:
                check_threshold(SymbolName, MystockPrice,stockNotificationType,notificationPayload,stockCheckInterval)
                now = datetime.now()
                next_minute = (now + timedelta(minutes=timer)).replace(second=0, microsecond=0)
                time_to_wait = (next_minute - now).total_seconds()
                time.sleep(time_to_wait)

#function to handle SMS
def check_threshold(SymbolName, MystockPrice,stockNotificationType,notificationPayload,stockCheckInterval):
    currentPrice = si.get_live_price(SymbolName)
    if currentPrice > MystockPrice:
        if(stockNotificationType=="Email"):
            print("Mailing Service")
            sendMail(notificationPayload,SymbolName,MystockPrice,currentPrice)
        else:
            print("SMS")  
            sendSMS(notificationPayload,SymbolName,MystockPrice,currentPrice)      
            
    else:
        print("Stock price is lower than threshold")      
#function to handle email       
def sendMail(notificationPayload,SymbolName,MystockPrice,currentPrice):
    sender_email = "usstockalerter@gmail.com"
    receiver_email = notificationPayload

    subject = "Stock Alert"
    message = "Stock price is higher than threshold. Symbol: "+SymbolName+" Threshold Price: "+str(MystockPrice)+" Current Price: "+str(currentPrice)
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, "aiigruiuswpusslo")
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)          
        
#function to handle sms
def sendSMS(notificationPayload,SymbolName,MystockPrice,currentPrice):
    #your Account SID and Auth Token 
    account_sid = 'AC0097621915f6378da39162bb2b78e263'
    auth_token = '97ffeae960d2f5d712cee8fa33620026'
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body="The stock price is higher than threshold. Symbol: "+SymbolName+" Threshold Price: "+str(MystockPrice)+" Current Price.",
            from_='+16074007517',
            to='+9779860999660'
        )