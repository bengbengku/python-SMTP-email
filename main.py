import pandas
import smtplib
import random
import datetime as dt
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

MY_EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

now = dt.datetime.now()
month = now.month
day = now.day

"""Setup tuple untuk bulan dan hari"""
today = (month, day)
print(today)
"""Gunakan module pandas untuk membaca data birthday.csv"""
data = pandas.read_csv("birthday.csv")

"""Dictionary comprehension untuk pandas dataframe"""
birthdays_dict = { (data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows() }
print(birthdays_dict)

if today in birthdays_dict:
    birthdays_persons = birthdays_dict[today]
    file_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"

    """Mengganti nama yang dituju dari data file"""
    with open(file_path) as letter_file:
        contents = letter_file.read()
        contents = contents.replace("[NAME]", birthdays_persons["name"])

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=birthdays_persons["email"],
            msg=f"Subject:[Sunday Motivation!]\n\n{contents}".encode("utf-8"),
        )