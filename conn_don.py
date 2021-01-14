import datetime
import flask_login
import pymongo

class Conn_don:
    @classmethod
    def connect(cls):
        cls.user = 'user'
        cls.password = 'userPassword'
        cls.database = 'promesse_don'
        return pymongo.MongoClient(f'mongodb+srv://{cls.user}:{cls.password}@cluster0.jkqtq.mongodb.net/{cls.database}?retryWrites=true&w=majority')

    @classmethod
    def open_connexion(cls):
        cls.client = cls.connect()
        cls.don = cls.client.promesse_don.don
        cls.users = cls.client.promesse_don.users

    @classmethod
    def close_connexion(cls):
        cls.client.close()

    @classmethod
    def get_count(cls):
        cls.open_connexion()
        count = cls.don.count_documents({})
        cls.close_connexion()
        return count

    @classmethod
    def get_don(cls):
        cls.open_connexion()
        don = list(cls.don.find())
        cls.close_connexion()
        return don

    @classmethod
    def insert(cls, name, firstname, adress, mail, somme):
        cls.datetime_now = datetime.datetime.now()
        cls.open_connexion()
        cls.don.insert({'name':name, 'firstname':firstname, 'adress':adress, 'mail':mail, 'donation':somme, 'date':cls.datetime_now})
        cls.close_connexion()

    @classmethod
    def total(cls):
        cls.open_connexion()
        total_raw = list(cls.don.aggregate([{'$group':{'_id': 'null', 'totalamount':{'$sum':"$donation"}}}]))
        total = total_raw[0]['totalamount']
        cls.close_connexion()
        return total

    @classmethod
    def find_user(cls, mail, password):
        cls.open_connexion()
        user = list(cls.users.find({'mail':mail, 'password':password}))
        cls.close_connexion()
        return user