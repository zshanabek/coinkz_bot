from celery import Celery

app = Celery('tasks', broker='amqp://localhost//', backend="db+mongo://mongodb://fuckingtelegramuser:fuckfuckfuck@ds059546.mlab.com:59546/fuckingtelegrambot")
@app.task 
def reverse(string):
    return string[::-1]
@app.task 
def add(x, y):
    return x + y