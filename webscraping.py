# Importing Libraries
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import sys
import os
import datetime
import calendar


def file_read_from_tail(fname, lines):
    bufsize = 8192
    fsize = os.stat(fname).st_size
    iter = 0
    with open(fname) as f:
        if bufsize > fsize:
            bufsize = fsize-1
            data = []
            while True:
                iter += 1
                f.seek(fsize-bufsize*iter)
                data.extend(f.readlines())
                if len(data) >= lines or f.tell() == 0:
                    return (''.join(data[-lines:]))


# Headers and login data to pass to the network. Make sure you use your own Header.
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
}

Username = raw_input("Enter your usernmae")
Password = raw_input("Enter your password")
login_data = {
    # 'pass_dup': '',
    'username': Username,
    'password': Password,
    # 'buttonName': '',
    'login-form-type': 'pwd'
}
with requests.Session() as s:
    url = 'https://www.smartmetertexas.com/pkmslogin.form'
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    r = s.post(url, data=login_data, headers=headers)

    content = r.text
    WebPageData = BeautifulSoup(content, 'html.parser')

    # Getting the Date and Meter Reading Data
    TotalMeterReadingData = WebPageData.find(lambda tag: tag.name == 'span' and tag.has_attr(
        'name') and tag['name'] == "ler_read")
    DateData = WebPageData.find(lambda tag: tag.name == 'span' and tag.has_attr(
        'name') and tag['name'] == "ler_date")
    # Assigning the values to an integer.
    TotalMeterReading = TotalMeterReadingData.text
    Date = DateData.text
    # print(Date)
    # print(TotalMeterReading)
# Writing the data to a file
try:
    data_file = open('data.txt', 'a')
except:
    print("Couldn't open the file")
else:
    last_line = file_read_from_tail('data.txt', 1)
    if (last_line == TotalMeterReading):
        print("No Update Available")
    else:
        data_file.write("\n"+Date+"\n"+TotalMeterReading)
        data_file.close()
        print("File Updated")

# Reading the Data From the File
lines = list(open('data.txt'))
length = len(lines)

# Reading the First and Last Meter Readings
Starting_String = lines[1]
Last_String = lines[length-1]

# Deleting the \n character
Starting = Starting_String.strip()
Last = Last_String.strip()

# Calculating the Number of Days Passed and Remaining
today = datetime.date.today()
days_in_current_month = calendar.monthrange(today.year, today.month)[1]
days_till_end_of_month = days_in_current_month-today.day
start_date = today + datetime.timedelta(days=days_till_end_of_month+8)
DaysRemaining = int((start_date-today).days)
# print(DaysRemaining)

# Calculating the Total Amount of Electricity Used and Remaining

Total_Used = float(Last)-float(Starting)
Remaining = 1000 - float(Total_Used) #CHANGE this 1000 to your preference. 
AverageUsePerDay = (Remaining)/DaysRemaining
CurrentUsePerDay = (Total_Used/(today.day-8))
# Printing out the final Results.
print("Total Electricity Usuage: "+format(Total_Used, '.2f'))
print("Remaining: "+format(Remaining, '.2f'))
print("Days Remaining", DaysRemaining)
print("Current Average Use per Day: " + format(CurrentUsePerDay, '.2f'))
print("Future Average Use Per Day: " + format(AverageUsePerDay, '.2f'))
