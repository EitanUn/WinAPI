"""
Author: Eitan Unger
Date: 08/11/22
Database class with file saving and writing capabilities, database is saved in database.bin, can be transferred
Inherits from DB, super of the IPC-sync database class
"""
from db import DB
from pickle import dump, load
import logging
import os

FILE = "database.bin"
FORMAT = '%(asctime)s.%(msecs)03d - %(message)s'
DATEFMT = '%H:%M:%S'


class FileDB(DB):
    """
    File Database class
    """
    def __init__(self):
        """
        Constructor for file database
        """
        super().__init__()
        if not os.path.exists(FILE):
            with open(FILE, "wb") as file:
                dump({}, file)

    def load(self):
        """
        Read database from the save file
        """
        with open(FILE, "rb") as file:
            logging.debug("File Database: Opened file %s for reading" % FILE)
            self.database = load(file)
            logging.debug("File Database: Loaded database from file " + FILE)

    def dump(self):
        """
        Write database to file
        """
        with open(FILE, "wb") as file:
            logging.debug("File Database: Opened file %s for writing" % FILE)
            dump(self.database, file)
            logging.debug("File Database: Updated database to file " + FILE)

    def set_value(self, key, val):
        """
        if key is a key in the database set the value to val, else add key: val as a pair to the db, and update the
        file accordingly
        :param key: key to check
        :param val: value to set
        :return: Succeeded (True/False)
        """
        try:
            self.load()
            res = super().set_value(key, val)
            self.dump()
            return res
        except OSError as err:
            logging.error("File Database: Got OSError %s while opening file %s, returning False for failure"
                          % (err, FILE))
            return False

    def get_value(self, key):
        """
        Return the value of key if it is a key in dict, else None
        :param key: key to check
        :return: self.database[key] if key is a key in the dict, else None
        """
        self.load()
        return super().get_value(key)

    def delete_value(self, key):
        """
        Deletes the value of key in the dict and returns it, if nonexistent raise KeyError
        :param key: key to check
        :return: deleted value if successful
        """
        self.load()
        res = super().delete_value(key)
        self.dump()
        return res


if __name__ == '__main__':
    logging.basicConfig(filename="FileDB.log", filemode="a", level=logging.DEBUG, format=FORMAT, datefmt=DATEFMT)
