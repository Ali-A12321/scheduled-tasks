import requests
import os
import smtplib
my_email = "pythonautomation74@gmail.com"
my_password = os.environ.get("SMTP_PASSWORD")
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
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        for email in emails:
            connection.sendmail(
            from_addr=my_email,
            to_addrs=email,
            msg=f"""Subject:{rain_str}: It is going to rain!\n\n
                It is going to rain at within:\n{rain_str2}.\nBring an umbrella!"""
        )