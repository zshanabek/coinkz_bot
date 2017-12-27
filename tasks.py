from celery import Celery

app = Celery('tasks', broker='amqp://')
@app.task 
def reverse(string):
    return string[::-1]
@app.task 
def add(x, y):
    return x + y