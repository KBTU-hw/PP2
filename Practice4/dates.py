import datetime

#1
print(datetime.date.today()-datetime.timedelta(days=5))
#2
yesterday=datetime.date.today()-datetime.timedelta(days=1)
today=datetime.date.today()
tomorrow=datetime.date.today()+datetime.timedelta(days=1)
print(yesterday, today, tomorrow)
#3
print(datetime.datetime.now().replace(microsecond=0))
#4
a, b, c=map(int, input().split())
x=datetime.date(a, b, c)
y=datetime.date.today()
delta=y-x
print(delta.days * 24 * 60 * 60)