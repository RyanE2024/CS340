from pymongo import MongoClient
from pymongo.errors import PyMongoError


class AnimalShelter(object):
    """CRUD operations for Animal collection in MongoDB"""

    def __init__(self, username="aacuser", password="SNHU1234",
                 host="localhost", port=27017, db="aac", col="animals"):
        """
        Initialize Mongo connection.
        Note: authSource is set to the same DB where the user was created ("aac").
        """
        self.USER = username
        self.PASS = password
        self.HOST = host
        self.PORT = port
        self.DB = db
        self.COL = col

        try:
            uri = f"mongodb://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/?authSource=admin"
            self.client = MongoClient(uri)
            self.database = self.client[self.DB]
            self.collection = self.database[self.COL]

            # Force a quick connection check
            self.client.admin.command("ping")

        except PyMongoError as e:
            raise RuntimeError(f"MongoDB connection failed: {e}")

    # C in CRUD
    def create(self, data):
        """
        Insert a document into the collection.
        Input: dictionary of key/value pairs
        Return: True if inserted, else False
        """
        if data is None or not isinstance(data, dict) or len(data) == 0:
            return False

        try:
            result = self.collection.insert_one(data)
            return result.acknowledged is True
        except PyMongoError:
            return False

    # R in CRUD
    def read(self, query):
        """
        Query documents using find() (NOT find_one()).
        Input: dictionary query filter
        Return: list of results if successful, else []
        """
        if query is None:
            query = {}

        if not isinstance(query, dict):
            return []

        try:
            cursor = self.collection.find(query)
            return list(cursor)
        except PyMongoError:
            return []
        
    def update(self, query, update_data):
        """
        Update document(s) in the collection.
        """
        if query is None or update_data is None:
            return 0

        if not isinstance(query, dict) or not isinstance(update_data, dict):
            return 0

        try:
            result = self.collection.update_many(query, update_data)
            return result.modified_count
        except PyMongoError:
            return 0


    def delete(self, query):
        """
        Delete document(s) from the collection.
        """
        if query is None:
            return 0

        if not isinstance(query, dict):
            return 0

        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except PyMongoError:
            return 0