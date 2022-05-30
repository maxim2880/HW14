import sqlite3


class DbConnect:
    def __init__(self, path):
        self.con = sqlite3.connect("netflix.db")
        self.cur = self.con.cursor()

    def __del__(self):
        self.cur.close()
        self.con.close()


def get_by_title(title):
    db_connect = DbConnect("netflix.db")
    db_connect.cur.execute(
        f"""SELECT title, country, release_year, listed_in,
     description from netflix 
     where title = {title}""")
