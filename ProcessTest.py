from syncdb import SyncDB
from filedb import FileDB
import multiprocessing
import logging

FORMAT = '%(asctime)s.%(msecs)03d - %(message)s'
DATEFMT = '%H:%M:%S'


def main():
    logging.debug("Starting tests for Multithreading")
    db = SyncDB(FileDB(), False)
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing simple write perms")
    p1 = multiprocessing.Process(target=SyncDB.set_value, args=(db, "test1", 1))
    p1.start()
    p1.join()
    logging.info("test successful")
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing simple read perms")
    p1 = multiprocessing.Process(target=SyncDB.get_value, args=(db, "test1"))
    p1.start()
    p1.join()
    logging.info("test successful")
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing read blocks writing")
    p1 = multiprocessing.Process(target=SyncDB.get_value, args=(db, "test1"))
    p2 = multiprocessing.Process(target=SyncDB.set_value, args=(db, "test2", 2))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    logging.info("test successful")
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing write blocks reading")
    p1 = multiprocessing.Process(target=SyncDB.set_value, args=(db, "test3", 3))
    p2 = multiprocessing.Process(target=SyncDB.get_value, args=(db, "test2"))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    logging.info("test successful")
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing multi reading perms possible")
    p1 = multiprocessing.Process(target=SyncDB.get_value, args=(db, "test3"))
    p2 = multiprocessing.Process(target=SyncDB.get_value, args=(db, "test4"))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    logging.info("test successful")
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing delete")
    p1 = multiprocessing.Process(target=SyncDB.delete_value, args=(db, "test1"))
    p2 = multiprocessing.Process(target=SyncDB.get_value, args=(db, "test1"))
    p3 = multiprocessing.Process(target=SyncDB.set_value, args=(db, "test1", 1))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing load")
    p1 = multiprocessing.Process(target=SyncDB.get_value, args=(db, "test1"))
    p2 = multiprocessing.Process(target=SyncDB.get_value, args=(db, "test3"))
    p3 = multiprocessing.Process(target=SyncDB.set_value, args=(db, "load", "abcabc"))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p1 = multiprocessing.Process(target=SyncDB.get_value, args=(db, "load"))
    p2 = multiprocessing.Process(target=SyncDB.get_value, args=(db, "test2"))
    p1.start()
    p2.start()
    p3.join()
    p1.join()
    p2.join()
    logging.info("test successful")


if __name__ == '__main__':
    logging.basicConfig(filename="ProcessTest.log", filemode="a", level=logging.DEBUG, format=FORMAT, datefmt=DATEFMT)
    main()
