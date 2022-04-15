import pymongo

username = 'florren'#os.environ.get("USERNAME")
password = 'florren2k2'#os.environ.get("PASSWORD")

class MyDatabase():
    cluster = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@cluster0.y5mnt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", connect = False)
    db = cluster.insta 
    def __init__(self):
        pass
    
    @classmethod
    def getCollection(self, name : str):
        return self.db[name]