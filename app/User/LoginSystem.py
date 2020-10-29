from app.database.dbManager import dbManager

from werkzeug.security import generate_password_hash, check_password_hash

class LoginSystem:
    #singleton class
    __instance__ = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if LoginSystem.__instance__ == None:
            LoginSystem()
        return LoginSystem.__instance__

    def __init__(self):
        """ Virtually private constructor. """
        if LoginSystem.__instance__ != None:
            raise Exception("This class is a singleton!")
        else:
            LoginSystem.__instance__ = self
            self.db = dbManager()
            self.table = 'accounts'



    def verifyLogin(self, username, password):
        account = self.db.search_data(self.table,'username' , username)
        if account:
            if check_password_hash(str(account['password_hash']), password):
                # the account exist
                return account
                # if bool(account['admin_auth']):
                #     # if the user is Admin user
                #     #create Admin Object
                #     return AdminUser(account['username'], account['id'],bool(account['admin_auth']))
                # else:
                #     # if the user is Normal user
                #     #create NormalUser Object
                #     return NormalUser(account['username'], account['id'],bool(account['admin_auth']))

        return None





