import smtplib as sm
import datetime as dt
import random as rd
import pandas as pd
import os

my_email = "pythonautomation74@gmail.com"
my_password = os.environ.get("SMTP_PASSWORD")
monday_emails = ["alihassanamin2012@gmail.com","23a.amin@preston-manor.com","mrhadiamin2007@gmail.com","fatimalissa@yahoo.co.uk","23f.burhan@preston-manor.com","samaatiah54@gmail.com"]
now = dt.datetime.now()
if now.weekday() == 0:
    with open("quotes.txt") as file:
        lines = file.readlines()
        quote = rd.choice(lines)
        with sm.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            for email in monday_emails:
                connection.sendmail(from_addr=my_email, to_addrs=email, msg=f"Subject:Monday Motivation!\n\n{quote}\nFrom Ali Amin")

today = (now.month, now.day)

data = pd.read_csv("birthdays.csv")
birthday_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}

if today in birthday_dict:
    with open(f"letter_templates/letter_{rd.randint(1,3)}.txt") as file:
        body = file.read()
        body = body.replace("[NAME]", birthday_dict[today]["name"])
    with sm.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email, to_addrs=birthday_dict[today]["email"], msg=f"Subject:Happy Birthday!\n\n{body}")