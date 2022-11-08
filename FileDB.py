"""
Author: Eitan Unger
Date: 08/11/22
Database class with file saving and writing capabilities, database is saved in database.bin, can be transferred
Inherits from DB, super of the IPC-sync database class
"""
from DB import DB
from pickle import dump, load

FILE = "database.bin"


class FileDB(DB):
    """
    File Database class
    """
    def __init__(self):
        """
        Constructor for file database
        """
        super().__init__()

    def load(self):
        """
        Read database from the save file
        """
        with open(FILE, "rb") as file:
            self.database = load(file)

    def dump(self):
        """
        Write database to file
        """
        with open(FILE, "wb") as file:
            dump(self.database, file)

    def set_value(self, key, val):
        """
        if key is a key in the database set the value to val, else add key: val as a pair to the db, and update the
        file accordingly
        :param key: key to check
        :param val: value to set
        :return: Succeeded (True/False)
        """
        self.load()
        res = super().set_value(key, val)
        self.dump()
        return res

    def get_value(self, key):
        self.load()
        return super().get_value(key)

    def delete_value(self, key):
        self.load()
        res = super().delete_value(key)
        self.dump()
        return res
