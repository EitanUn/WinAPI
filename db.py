"""
Author: Eitan Unger
Date: 08/11/22
Base Database class for the IPC-sync database project, very similar to a regular dictionary
"""

import logging
FORMAT = '%(asctime)s.%(msecs)03d - %(message)s'
DATEFMT = '%H:%M:%S'


class DB:
    """
    Base database class
    """
    def __init__(self):
        """
        Constructor for DB class
        """
        logging.debug("Database: Created database")
        self.database = {}

    def set_value(self, key, val):
        """
        If key is a key in the database dictionary, change its value to val. Else, add key: val as a pair to the dict
        :param key: key to check
        :param val: value to set
        :return: succeeded (True/False)
        """
        # logging.info("Database: Set value of key %s to %s" % (str(key), str(val)))
        self.database.update({key: val})
        return True

    def get_value(self, key):
        """
        Return the value of key if it is a key in dict, else None
        :param key: key to check
        :return: self.database[key] if key is a key in the dict, else None
        """
        if key in self.database.keys():
            # logging.info("Database: Got value at key %s" % str(key))
            return self.database[key]
        else:
            # logging.warning("Database: Tried to get value at nonexistent key %s, returned None instead" % str(key))
            return None

    def delete_value(self, key):
        """
        Deletes the value of key in the dict and returns it, if nonexistent raise KeyError
        :param key: key to check
        :return: deleted value if successful
        """
        try:
            # logging.info("Database: Tried to delete value at key %s" % str(key))
            return self.database.pop(key)
        except KeyError:
            # logging.error("Database: Tried to delete value at nonexistent key %s, returned None instead" % str(key))
            return None

    def __str__(self):
        """
        tostring function for database type
        """
        return str(self.database)


if __name__ == '__main__':
    logging.basicConfig(filename="DB.log", filemode="a", level=logging.DEBUG, format=FORMAT, datefmt=DATEFMT)
