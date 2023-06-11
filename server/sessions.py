import base64, os

class SessionStore:

    def __init__(self):
        #a dictionary: keys are session IDs, values are dictionaries for the session data
        self.sessions = {}

    #other methodes

    def generateSessionId(self):
        x = os.urandom(32)
        rstr = base64.b64encode(x).decode("utf-8")
        return rstr

    def createSession(self):
        sessionId = self.generateSessionId()
        self.sessions[sessionId] = {}
        return sessionId

    #return the session data associated to the given ID
    def getSessionData(self, sessionId):
        if sessionId in self.sessions:
            return self.sessions[sessionId]
        else:
            return None
    
    #optional
    def storeSessionData(self, sessionID, data):
        pass
    #optional
    def storeSessionDataUserID(self, sessionID, userID):
        pass
    #optional
    def clearSession(self, sessionId):
        pass
    #optional
    def doesSessionExist(self, sessionID):
        pass
