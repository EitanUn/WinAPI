"""
Author: Eitan Unger
Date: 13/12/22
Synchronous database class using winAPI Semaphores and Mutex.
Database is saved in database.bin, can be transferred, using FileDB as the database itself.
"""

from filedb import FileDB
import logging
from win32event import CreateMutex, CreateSemaphore, WaitForSingleObject, ReleaseMutex, ReleaseSemaphore, INFINITE

FORMAT = '%(asctime)s.%(msecs)03d - %(message)s'
DATEFMT = '%H:%M:%S'
READNAME = "read"
WRITENAME = "write"


class SyncDB:
    def __init__(self, db: FileDB):
        self.database = db
        self.read = CreateSemaphore(None, 10, 10, READNAME)
        self.write = CreateMutex(None, False, WRITENAME)

    def read_get(self):
        WaitForSingleObject(self.read, INFINITE)
        logging.debug("Sync Database: acquired reading permissions")

    def read_release(self):
        ReleaseSemaphore(self.read)
        logging.debug("Sync Database: released reading permissions")

    def write_get(self):
        WaitForSingleObject(self.write, INFINITE)
        for i in range(10):
            WaitForSingleObject(self.read, INFINITE)
        logging.debug("Sync Database: acquired writing permissions")

    def write_release(self):
        for i in range(10):
            ReleaseSemaphore(self.read)
        ReleaseMutex(self.write)
        logging.debug("Sync Database: released writing permissions")

    def set_value(self, key, val):
        self.write_get()
        res = self.database.set_value(key, val)
        self.write_release()
        return res

    def get_value(self, key):
        self.read_get()
        res = self.database.get_value(key)
        self.read_release()
        return res

    def delete_value(self, key):
        self.write_get()
        self.database.delete_value(key)
        self.write_release()


if __name__ == '__main__':
    logging.basicConfig(filename="SyncDB.log", filemode="a", level=logging.DEBUG, format=FORMAT, datefmt=DATEFMT)
