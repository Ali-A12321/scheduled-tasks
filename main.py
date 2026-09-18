import requests
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

OWM_endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWM_API_KEY")
with open("rain_emails.txt") as file:
    emails = file.readlines()
MY_LAT = 51.564072
MY_LNG = -0.295402
weather_parameters = {
    "lat":MY_LAT,
    "lon":MY_LNG,
    "appid":api_key,
    "cnt":4
}
response = requests.get(OWM_endpoint, params=weather_parameters)
response.raise_for_status()
weather_data = response.json()
will_rain = False
idx=0
rain_indexes=[]
for dict in weather_data["list"]:
    if dict["weather"][0]["id"] < 700:
        will_rain = True
        rain_indexes.append(f"{idx}-{idx+3}hrs")
    idx += 3
rain_str = ", ".join(rain_indexes)
rain_str2 = "\n".join(rain_indexes)

if will_rain:
    with sm.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        for email in emails:
            connection.sendmail(
            from_addr=my_email,
            to_addrs=email,
            msg=f"""Subject:{rain_str}: It is going to rain!\n\n
                It is going to rain at within:\n{rain_str2}.\nBring an umbrella!"""
        )
