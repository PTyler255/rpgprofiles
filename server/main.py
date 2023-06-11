from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import json
import sys
from urllib.parse import parse_qs
from players_db import *
from http import cookies
from passlib.hash import bcrypt
from sessions import *

'''
    method POST (optionally delete
    path: /sessions

    parse body
    find user in DB by email
    if exists?:
        verify password against hash in in DB
        if verified:
            Success 201
        else:
            Fail 401  
    else:
        Fail 401
'''

SESSION_STORE = SessionStore()


class MyRequestHandler(BaseHTTPRequestHandler):
   #load cookie data from client via the Cookie Header
    def load_cookie(self):
        print("request headers: ", self.headers)
        cookie_data = self.headers["Cookie"]
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(cookie_data)
        else:
            self.cookie = cookies.SimpleCookie()

    #send cookie data to client via the Set-Cookie header
    def send_cookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())

    #load the sesion data for the current client self.sessionData
    def load_session(self):
        self.load_cookie()
        #check the cookie data to find a session ID
        if "sessionID" in self.cookie:
            sessionID = self.cookie["sessionID"].value
            self.sessionData = SESSION_STORE.getSessionData(sessionID)
            #if sessionData cannot be loaded (Session ID is invalid)
            if not self.sessionData:
                sessionID = SESSION_STORE.createSession()
                self.cookie["sessionID"] = sessionID
                self.sessionData = SESSION_STORE.getSessionData(sessionID)
        else: # 
            sessionID = SESSION_STORE.createSession()
            self.cookie["sessionID"] = sessionID
            self.sessionData = SESSION_STORE.getSessionData(sessionID)
        self.cookie["sessionID"]["samesite"] = "None"
        self.cookie["sessionID"]["secure"] = True


    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_cookie()
        super().end_headers()

    def verifyUser(self):
        udb = UsersDB()
        if "userID" in self.sessionData:
            userID = self.sessionData["userID"]
            user = udb.findUserByID(userID)
            if user:
                return True
        else:
            return False

    #handle methods

    def handleGetPlayers(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        pdb =  PlayersDB()
        players = pdb.getAllPlayers()
        self.wfile.write(bytes(json.dumps(players), "utf-8"))
    
    def handleGetPlayer(self, member_id):
        pdb = PlayersDB()
        player = pdb.getOnePlayer(member_id)
        #check if id is valid
        if player != None:
            #restaurant exists
            #respond with 200 and data
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(player), "utf-8"))
        else:
            #retaurant does not exist
            #respond with 200 and data
            self.handleNotFound()
        #query the DB for the character member (using id`
        #response: status, header, body

    def handleCreatePlayer(self):
        # Get incoming request body
        length = int(self.headers["Content-Length"])
        request_body=self.rfile.read(length)
        # parse the request body (urlencoded data)
        parsed_body = parse_qs(request_body)
        # retrieve character data from the parsed body
        pname = parsed_body[b'name'][0]
        pclass = parsed_body[b'class'][0]
        plevel = parsed_body[b'level'][0]
        pmoney = parsed_body[b'money'][0]
        presource = parsed_body[b'resource'][0]
        pnotes = parsed_body[b'notes'][0]
        
        pname = pname.decode('ascii')
        pclass = pclass.decode('ascii')
        plevel = int(plevel.decode('ascii'))
        pmoney = float(pmoney.decode('ascii'))
        presource = int(presource.decode('ascii'))
        pnotes = pnotes.decode('ascii')
        # append the new restaurant to the list
        pdb = PlayersDB()
        pdb.createPlayers(pname, plevel, pclass, pmoney, presource, pnotes)
        self.send_response(201)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Added", "utf-8"))

    def handleUpdatePlayer(self, pid):
        pdb = PlayersDB()
        if pdb.getOnePlayer(pid):
            # Get incoming request body
            length = int(self.headers["Content-Length"])
            request_body=self.rfile.read(length)
            # parse the request body (urlencoded data)
            parsed_body = parse_qs(request_body)
            # retrieve character data from the parsed body
            pname = parsed_body[b'name'][0]
            pclass = parsed_body[b'class'][0]
            plevel = parsed_body[b'level'][0]
            pmoney = parsed_body[b'money'][0]
            presource = parsed_body[b'resource'][0]
            pnotes = parsed_body[b'notes'][0]
            
            pname = pname.decode('ascii')
            pclass = pclass.decode('ascii')
            plevel = int(plevel.decode('ascii'))
            pmoney = float(pmoney.decode('ascii'))
            presource = int(presource.decode('ascii'))
            pnotes = pnotes.decode('ascii')
            # append the new restaurant to the list
            pdb.updatePlayer(pid, pname, plevel, pclass, pmoney, presource, pnotes)
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("Added", "utf-8"))
        else:
            self.handleNotFound()
            
    def handleDeletePlayer(self, ide):
        pdb = PlayersDB()
        player = pdb.getOnePlayer(ide)
        #check if id is valid
        if player != None:
            #restaurant exists
            #respond with 200 and data
            pdb.deletePlayer(ide)
            self.send_response(200)
            self.end_headers()
        else:
            #retaurant does not exist
            #respond with 200 and data
            self.handleNotFound()

    def handleCreateUser(self):
        udb = UsersDB()
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        parsed_body = parse_qs(request_body)

        user_email = parsed_body['email'][0]
        user_password = parsed_body['password'][0]
        fname = parsed_body['fname'][0]
        lname = parsed_body['lname'][0]
        user = udb.findUserByEmail(user_email)
        if user:
            self.handleNotFound()
        else:
            hashword = bcrypt.hash(user_password)
            udb.createUser(user_email, fname, lname, hashword)
            self.send_response(201)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("User added", "utf-8"))

    def handleAuthenticateUser(self):    
        udb = UsersDB()
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        parsed_body = parse_qs(request_body)
        user_email = parsed_body['email'][0]
        user_password = parsed_body['password'][0]
        user = udb.findUserByEmail(user_email)
        if user:
            if bcrypt.verify(user_password, user['pw']):
                self.sessionData["userID"] = user["id"]
                self.send_response(201)
                self.end_headers()
            else:
                self.handleNotAllowed()
        else:
            self.handleNotAllowed()

    #do functions
    
    def do_OPTIONS(self):
        self.load_session()
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.end_headers()
    
    def do_GET(self):
        self.load_session()
        if self.verifyUser():
            #"This code will handle all incoming GET requests."
            #"The request path is: "
            parts = self.path[1:].split("/")
            collection_name =  parts[0]
            try:
                member_id = parts[1]
            except IndexError:
                member_id = None
            if collection_name == "PLAYERS":
                if member_id:
                    self.handleGetPlayer(member_id)
                else:
                    self.handleGetPlayers()
            else:
                self.handleNotFound()
        else:
            self.handleNotAllowed()
            
    def do_POST(self):
        self.load_session()
        if self.path == "/SESSIONS":
            self.handleAuthenticateUser()
        elif self.path == "/USERS":
            self.handleCreateUser()
        elif self.path == "/PLAYERS":
            if self.verifyUser():
                self.handleCreatePlayer()
            else:
                self.handleNotAllowed()
        else:
            self.handleNotFound()
    
    def do_PUT(self):
        self.load_session()
        if self.verifyUser():
            parts = self.path[1:].split("/")
            collection_name =  parts[0]
            try:
                member_id = parts[1]
            except IndexError:
                member_id = None
            if collection_name == "PLAYERS":
                if member_id:
                    self.handleUpdatePlayer(member_id)
                else:
                    self.handleNotFound()
            elif collection_name == "SESSIONS":
                self.handleGetSessions()
            else:
                self.handleNotFound()
        else:
            self.handleNotAllowed()

    def do_DELETE(self):
        self.load_session()
        if self.verifyUser():
            parts = self.path[1:].split("/")
            collection_name =  parts[0]
            try:
                member_id = parts[1]
            except IndexError:
                member_id = None
            if collection_name == "PLAYERS":
                if member_id:
                    self.handleDeletePlayer(member_id)
                else:
                    self.handleNotFound()
            else:
                self.handleNotFound()
        else:
            self.handleNotAllowed()

    def handleNotFound(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not found.", "utf-8"))
        
    def handleNotAllowed(self):
        self.send_response(401)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not allowed.", "utf-8"))

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass # no implementation

def run():
    db = PlayersDB()
    db.createPlayersTable()
    db = None #disconnect 
    udb = UsersDB()
    udb.createUserTable()
    udb = None
    port = 8080
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    listen = ("0.0.0.0", port)
    server = ThreadedHTTPServer(listen, MyRequestHandler) 
    print("The Server is running!")
    server.serve_forever()
    
if __name__ == '__main__':
    run()
#http://localhost:8080
