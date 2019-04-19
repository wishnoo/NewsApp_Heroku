from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import sys,os
import json
import datetime
import time
text = "text"
# sched = BlockingScheduler()
# @sched.scheduled_job('interval', minutes=30)
def timed_job():
    top = open(os.path.join(text,"news.txt"), "w+")
    r = requests.get('https://newsapi.org/v2/top-headlines?country=us&apiKey=13ed18aed5aa424bb3afa52a4bfde4fe')
    data = r.json()
    top.write(json.dumps(data))
    top.close()

    #<------ write the data where category is business ------>
    business = open(os.path.join(text,"business.txt"),"w+")
    r = requests.get('https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=13ed18aed5aa424bb3afa52a4bfde4fe')
    data = r.json()
    business.write(json.dumps(data))
    business.close()

    #<------ write the data where category is science ------>
    science = open(os.path.join(text,"science.txt"),"w+")
    r = requests.get('https://newsapi.org/v2/top-headlines?country=us&category=science&apiKey=13ed18aed5aa424bb3afa52a4bfde4fe')
    data = r.json()
    science.write(json.dumps(data))
    science.close()

    #<------ write the data where category is health ------>
    health = open(os.path.join(text,"health.txt"),"w+")
    r = requests.get('https://newsapi.org/v2/top-headlines?country=us&category=health&apiKey=13ed18aed5aa424bb3afa52a4bfde4fe')
    data = r.json()
    health.write(json.dumps(data))
    health.close()

    #<------ write the data where category is sports ------>
    sports = open(os.path.join(text,"sports.txt"),"w+")
    r = requests.get('https://newsapi.org/v2/top-headlines?country=us&category=sports&apiKey=13ed18aed5aa424bb3afa52a4bfde4fe')
    data = r.json()
    sports.write(json.dumps(data))
    sports.close()

    #<------ write the data where category is technology ------>
    technology = open(os.path.join(text,"technology.txt"),"w+")
    r = requests.get('https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey=13ed18aed5aa424bb3afa52a4bfde4fe')
    data = r.json()
    technology.write(json.dumps(data))
    technology.close()

    #<------ Update time print ------>
    print("Updated on: ",datetime.datetime.now(),"!!!!")

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(timed_job, 'interval', minutes=30)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
