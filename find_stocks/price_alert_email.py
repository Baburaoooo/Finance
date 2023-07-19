import os
import smtplib
from email.message import EmailMessage
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
import time

# Get email address and password from environment variables
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

# Function to send email
def send_email(subject, content, files=[]):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ''
    msg.set_content(content)

    for file_path in files:
        with open(file_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(file_path)
            msg.add_attachment(file_data, maintype='application', subtype='ocetet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print("Email sent.")

# Set the stock and the target price
stock = "QQQ"
target_price = 180

# Set the start date and current date
start = dt.datetime(2018, 12, 1)
now = dt.datetime.now()

# Initialize the alerted flag
alerted = False

while True:
    # Get the stock data from Yahoo Finance API
    df = pdr.get_data_yahoo(stock, start, now)

    # Get the current close price
    current_close = df["Adj Close"][-1]

    # Check if the current close price is greater than the target price and if alerted flag is False
    if current_close > target_price and not alerted:
        # Set the alerted flag to True and create the message
        alerted = True
        message = f"{stock} has activated the alert price of {target_price}\nCurrent Price: {current_close}"
        print(message)

        # Send the email message
        send_email('Alert on ' + stock + '!', message, files=[r""])  # Add file path if needed

    else:
        # Print if there are no new alerts
        print("No new alerts")

    # Wait for 60 seconds before checking again
    time.sleep(60)
