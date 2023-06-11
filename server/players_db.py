import os
import psycopg2
import psycopg2.extras
import urllib

#def dict_factory(cursor, row):
#    d = {}
#    for idx, col in enumerate(cursor.description):
#        d[col[0]] = row[idx]
#    return d

#swap %s for %s

class PlayersDB:

    def __init__(self):
        #self.connection = sqlite3.connect('players_db.db')
        #self.connection.row_factory = dict_factory
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        self.connection = psycopg2.connect(#"players_db.db")
            cursor_factory=psycopg2.extras.RealDictCursor,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.cursor = self.connection.cursor()
        self.createPlayersTable()
    
    def __del__(self):
        self.connection.close()

    def createPlayersTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS players (id SERIAL PRIMARY KEY, name TEXT, class TEXT, level TEXT, money FLOAT, resource INT, notes TEXT)")
        #swap integer primary key with serial primary key
        self.connection.commit()

    def getAllPlayers(self):
        self.cursor.execute("SELECT * FROM players")
        players = self.cursor.fetchall()
        return players

    def getOnePlayer(self, player_id):
        data = [player_id]
        self.cursor.execute("SELECT * FROM players WHERE id = %s", data)
        player = self.cursor.fetchone()
        return player

    def createPlayers(self, n, l, c, m, r, no):
        data = [n, l, c, m, r, no]
        self.cursor.execute("INSERT INTO players (name, level, class, money, resource, notes) VALUES (%s, %s, %s, %s, %s, %s)", data)
        self.connection.commit()
        
    def deletePlayer(self, ide):
        data = [ide]
        self.cursor.execute("DELETE FROM players WHERE id = %s", data)
        self.connection.commit()
        
    def updatePlayer(self, ide, n, l, c, m, r, no):
        data = [n, l, c, m, r, no, ide]
        self.cursor.execute("UPDATE players SET name = %s, level = %s, class = %s, money = %s, resource = %s, notes =%s WHERE id = %s", data)
        self.connection.commit()


class UsersDB:

    def __init__(self):
        #self.connection = sqlite3.connect('players_db.db')
        #self.connection.row_factory = dict_factory
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        self.connection = psycopg2.connect(#"players_db.db")
            cursor_factory=psycopg2.extras.RealDictCursor,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.cursor = self.connection.cursor()
        self.createUserTable()
    
    def __del__(self):
        self.connection.close()
    
    def createUserTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, email TEXT, fname TEXT, lname TEXT, pw CHAR(60))")
        #swap integer primary key with serial primary key
        self.connection.commit()
        
    def findUserByEmail(self, ema):
        data = [ema]
        self.cursor.execute("SELECT * FROM users WHERE email = %s", data)
        user = self.cursor.fetchone()
        return user
    
    def findUserByID(self, ide):
        data = [ide]
        self.cursor.execute("SELECT * FROM users WHERE id = %s", data)
        user = self.cursor.fetchone()
        return user

    def createUser(self, ema, fn, ln, pw):
        data = [ema, fn, ln, pw]
        self.cursor.execute("INSERT INTO users (email, fname, lname, pw) VALUES (%s, %s, %s, %s)", data)
        self.connection.commit()


'''
    def createRestauraunts(self, name, level, clss, money, resources):
        data = [name, level, clss, money, resources]
        self.cursor.execute("INSERT INTO players (name, level, class, money, resource, notes, image ) VALUES (%s, %s, %s, %s, %s)", data)
        self.connection.commit()
'''

