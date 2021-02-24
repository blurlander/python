import requests
from bs4 import BeautifulSoup
import sqlite3

url = "https://www.imdb.com/chart/top"
response = requests.get(url)
html_cont = response.content


soup = BeautifulSoup(html_cont,"html.parser")
names = soup.find_all("td", {"class", "titleColumn"})
ratings = soup.find_all("td", {"class", "ratingColumn imdbRating"})


con = sqlite3.connect("demo_data.db")

cursor = con.cursor()


def create_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS IMDB_top_250 (Rank INT,Name TEXT,Rating REAL)")
    con.commit()


def add_data(rank,name,rating):
    cursor.execute("INSERT INTO IMDB_top_250 VALUES(?,?,?)",(rank,name,rating))
    con.commit()


def select_data():
    cursor.execute("SELECT * FROM IMDB_top_250")
    movies = cursor.fetchall()
    print(movies)
    con.commit()


def delete_all_data():
    cursor.execute("DELETE FROM IMDB_top_250")
    con.commit()



create_table()
delete_all_data()


for name, rating in zip(names, ratings):
    name = name.text.replace(".", "")
    rating = rating.text
    newtxt = name.split()
    rating = rating.split()
    name1 = ' '.join(newtxt[1:-1])
    add_data(int(newtxt[0]),name1,float(rating[0]))




