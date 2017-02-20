import datetime

x = datetime.datetime.now()
x=str(x)
x = x[:19]
today = datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
print today

beginDate = today + datetime.timedelta(days=-5)
print beginDate
