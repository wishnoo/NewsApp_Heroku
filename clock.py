from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import sys
import os
import json
import datetime
import time
import mysql.connector


# # ----- Path of the text file
# text = "text"


# sched = BlockingScheduler()
# @sched.scheduled_job('interval', minutes=30)
def timed_job():
    #----- config MySQL
    #----- Created an environmental variable in heruko named ENV
    if os.environ.get('ENV') == 'production':
        mydb = mysql.connector.connect(
            host="us-cdbr-iron-east-02.cleardb.net",
            user="b49bf4e8ca29d1",
            passwd="fcded3ea",
            database="heroku_b4f7e73acc276ba"
        )
    else:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="flaskdb"
        )

    # if(mydb):
    #     print("connection successfull")
    # else:
    #     print("Not successfull")

    # -----store the headlines into the database
    r = requests.get(
        'https://newsapi.org/v2/top-headlines?country=us&apiKey=13ed18aed5aa424bb3afa52a4bfde4fe')
    data = r.json()
    news = data['articles']
    cur = mydb.cursor()
    for item in news:
        sql = "INSERT IGNORE INTO news values (%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (item['url'], item['source']['name'], item['author'], item['title'],
               item['description'], item['urlToImage'], item['publishedAt'], item['content'])
        cur.execute(sql, val)
    mydb.commit()
    cur.close()

    # # ----- Select the last 20 articles from the news table
    # cur = mydb.cursor()
    # sql = "SELECT * FROM news ORDER BY publishedAt DESC LIMIT 20"
    # cur.execute(sql)
    # myresult = cur.fetchall()
    # # print (myresult)
    # cur.close()

    # # ------ Insert the 20 articles into the file news
    # top = open(os.path.join(text,"news.txt"), "w+")
    # list = []
    # print('myresult',myresult)
    # for first in myresult:
    #     dict = {}
    #     dict['url'] = first[0]
    #     dict['name'] = first[1]
    #     dict['author'] = first[2]
    #     dict['title'] = first[3]
    #     dict['description'] = first[4]
    #     dict['urlToImage'] = first[5]
    #     dict['publishedAt'] = first[6]
    #     dict['content'] = first[7]
    #     list.append(dict)
    # # print('list',list)
    # top.write(json.dumps(list))
    # top.close()

    # <------ write the data where category is business ------>
    r = requests.get(
        'https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=13ed18aed5aa424bb3afa52a4bfde4fe')
    data = r.json()
    business = data['articles']
    cur = mydb.cursor()
    for item in business:
        sql = "INSERT IGNORE INTO business values (%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (item['url'], item['source']['name'], item['author'], item['title'],
               item['description'], item['urlToImage'], item['publishedAt'], item['content'])
        cur.execute(sql, val)
    mydb.commit()
    cur.close()

    # <------ write the data where category is science ------>
    r = requests.get(
        'https://newsapi.org/v2/top-headlines?country=us&category=science&apiKey=13ed18aed5aa424bb3afa52a4bfde4fe')
    data = r.json()
    science = data['articles']
    cur = mydb.cursor()
    for item in science:
        sql = "INSERT IGNORE INTO science values (%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (item['url'], item['source']['name'], item['author'], item['title'],
               item['description'], item['urlToImage'], item['publishedAt'], item['content'])
        cur.execute(sql, val)
    mydb.commit()
    cur.close()

    # <------ write the data where category is health ------>
    r = requests.get(
        'https://newsapi.org/v2/top-headlines?country=us&category=health&apiKey=13ed18aed5aa424bb3afa52a4bfde4fe')
    data = r.json()
    health = data['articles']
    cur = mydb.cursor()
    for item in health:
        sql = "INSERT IGNORE INTO health values (%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (item['url'], item['source']['name'], item['author'], item['title'],
               item['description'], item['urlToImage'], item['publishedAt'], item['content'])
        cur.execute(sql, val)
    mydb.commit()
    cur.close()

    # <------ write the data where category is sports ------>
    r = requests.get(
        'https://newsapi.org/v2/top-headlines?country=us&category=sports&apiKey=13ed18aed5aa424bb3afa52a4bfde4fe')
    data = r.json()
    sports = data['articles']
    cur = mydb.cursor()
    for item in sports:
        sql = "INSERT IGNORE INTO sports values (%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (item['url'], item['source']['name'], item['author'], item['title'],
               item['description'], item['urlToImage'], item['publishedAt'], item['content'])
        cur.execute(sql, val)
    mydb.commit()
    cur.close()

    # <------ write the data where category is technology ------>
    r = requests.get(
        'https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey=13ed18aed5aa424bb3afa52a4bfde4fe')
    data = r.json()
    technology = data['articles']
    cur = mydb.cursor()
    for item in technology:
        sql = "INSERT IGNORE INTO technology values (%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (item['url'], item['source']['name'], item['author'], item['title'],
               item['description'], item['urlToImage'], item['publishedAt'], item['content'])
        cur.execute(sql, val)
    mydb.commit()
    cur.close()

    # <------ Update time print ------>
    print("Updated on: ", datetime.datetime.now(), "!!!!")


if __name__ == '__main__':
    # timed_job()
    scheduler = BlockingScheduler()
    scheduler.add_job(timed_job, 'interval', minutes=30)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
