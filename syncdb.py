import threading
import multiprocessing
from filedb import FileDB
import logging
from win32event import CreateMutex, CreateSemaphore, WaitForSingleObject, ReleaseMutex, ReleaseSemaphore, \
    OpenMutex, OpenSemaphore, SYNCHRONIZE

FORMAT = '%(asctime)s.%(msecs)03d - %(message)s'
DATEFMT = '%H:%M:%S'
READNAME = "read"
WRITENAME = "write"


class SyncDB:
    def __init__(self, db: FileDB):
        self.database = db
        CreateSemaphore(None, 0, 10, READNAME)

    def read_get(self):
        WaitForSingleObject(OpenSemaphore(SYNCHRONIZE, True, READNAME))
        logging.debug("Sync Database: acquired reading permissions")

    def read_release(self):
        ReleaseSemaphore(OpenSemaphore(SYNCHRONIZE, True, READNAME))
        logging.debug("Sync Database: released reading permissions")

    def write_get(self):
        self.write.acquire()
        for i in range(10):
            self.read.acquire()
        logging.debug("Sync Database: acquired writing permissions")

    def write_release(self):
        for i in range(10):
            self.read.release()
        self.write.release()
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
