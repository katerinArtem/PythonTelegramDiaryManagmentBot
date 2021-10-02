class User:
    userStatus = ""
    userPassword = ""
    def __init__(self,userStatus,userPassword):
        self.userStatus = userStatus
        self.userPassword = userPassword
    def __getstate__(self)->dict:
        state = {}
        state["userStatus"] =self.userStatus
        state["userPassword"] =self.userPassword
        return state
    def __setstate__(self,state:dict):
        self.userStatus = state["userStatus"]
        self.userPassword = state["userPassword"]
    def check_pass(self,pw)->bool:
        return pw == self.userPassword

class Users:
    users = {}
    def __init__(self):
        pass
    def __getstate__(self)->dict:
        state = {}
        state["users"] = self.users
        return state
    def __setstate__(self,state:dict):
        self.users = state["users"]
    def add_user(self,uS,uP,uId):
        if uId not in self.users: self.users[uId] = User(userStatus=uS,userPassword=uP)
    def check(self,uId)->bool:
        return uId in self.users
    def delete_user(self,uId):
        if uId in self.users: del self.users[uId]
    def get_user(self,uId)->User:
        return self.users[uId]  
    