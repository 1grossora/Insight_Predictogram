import os 
import requests
from bs4 import BeautifulSoup
import csv

def make_date_like(mysoup):
    script = mysoup.find_all("script",type='text/javascript')
    date = []
    Nuser = []
    for s in script:
        if len(s)==0 :
            continue
        mystring = unicode(s.contents[0])
        if len(mystring.split("+"))<30:
            continue
        for ss in mystring.split("+"):
            split_com =ss.split(',')
            if len(split_com)!=2:
                continue
            mydate = str(split_com[0])[2:]
            date.append(mydate)
            Nuser.append( int(ss.split(",")[1].split("\\")[0]))
    return date , Nuser

def csv_for_user(user):
    my_insta_url ="https://socialblade.com/instagram/user/{}".format(user)
    # make the soup
    req = requests.get(my_insta_url)
    tempsoup = BeautifulSoup(req.content, 'lxml')
    date , followers = make_date_like(tempsoup)
    # Write the files to a user specific csv
    with open('../data/follower_csv/followers_of_{}.csv'.format(user),"w+") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(zip(date,followers))


user = 'groryangro'

csv_for_user(user)

