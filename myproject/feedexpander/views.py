from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from models import User, Tweet
from bs4 import BeautifulSoup
import urllib
import feedparser

# Create your views here.


def feed(request, username):
    url = "https://twitrss.me/twitter_user_to_rss/?user=" + username
    dicc = feedparser.parse(url)
    out = ""

    for number in range(5):
        out += dicc.entries[number].title + "<br>"
        #Obtener las urls del tweet si hay
        urls = dicc.entries[number].title.split()
        for i in urls:
            if i.startswith("http://") or i.startswith("https://"):
                i = i.split('&')[0]
                out += "<li><a href=" + i + ">" + i + "</a></li>"
                #Obtener primer elemento <p>
                soup = BeautifulSoup(urllib.urlopen(i).read())
                out += str(soup.p).decode('utf8')
                #Obtener primer elemento <img>
                out += str(soup.img).decode('utf8') + "<br><br>"

        #Comprobar y guardar autor del tweet
        user = dicc.entries[number].title.split(':')[0]
        try:
            p = User.objects.get(name=user)
        except ObjectDoesNotExist:
            p = User(name=user)
            p.save()

        #Comprobar y guardar tweet
        try:
            t = Tweet.objects.get(content=dicc.entries[number].title)
        except ObjectDoesNotExist:
            t = Tweet(content=dicc.entries[number].title, url= dicc.entries[number].link, name=p)
            t.save()

    return HttpResponse(out)
