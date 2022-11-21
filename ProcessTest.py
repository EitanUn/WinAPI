from syncdb import SyncDB
from filedb import FileDB
import multiprocessing
import logging

FORMAT = '%(asctime)s.%(msecs)03d - %(message)s'
DATEFMT = '%H:%M:%S'


def test_write(db):
    logging.debug("started write test")
    for i in range(1000):
        if not db.set_value(i, "test" + str(i)):
            logging.error("error with setvalue")


def test_read(db):
    logging.debug("started read test")
    for i in range(1000):
        if not "test" + str(i) == db.get_value(i):
            logging.error("error with getvalue")


def main():
    logging.debug("Starting tests for Multithreading")
    db = SyncDB(FileDB(), False)
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing simple write perms")
    p1 = multiprocessing.Process(target=test_write, args=(db, ))
    p1.start()
    p1.join()
    logging.info("test successful")
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing simple read perms")
    p1 = multiprocessing.Process(target=test_read, args=(db, ))
    p1.start()
    p1.join()
    logging.info("test successful")
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing read blocks writing")
    p1 = multiprocessing.Process(target=test_read, args=(db, ))
    p2 = multiprocessing.Process(target=test_write, args=(db, ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    logging.info("test successful")
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing write blocks reading")
    p1 = multiprocessing.Process(target=test_write, args=(db, ))
    p2 = multiprocessing.Process(target=test_read, args=(db, ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    logging.info("test successful")
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing multi reading perms possible")
    p1 = multiprocessing.Process(target=test_read, args=(db, ))
    p2 = multiprocessing.Process(target=test_read, args=(db, ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    logging.info("test successful")
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing load")
    p1 = multiprocessing.Process(target=test_read, args=(db, ))
    p2 = multiprocessing.Process(target=test_read, args=(db, ))
    p3 = multiprocessing.Process(target=test_write, args=(db, ))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p1 = multiprocessing.Process(target=test_read, args=(db, ))
    p2 = multiprocessing.Process(target=test_read, args=(db, ))
    p1.start()
    p2.start()
    p3.join()
    p1.join()
    p2.join()
    logging.info("test successful")


if __name__ == '__main__':
    logging.basicConfig(filename="ProcessTest.log", filemode="a", level=logging.DEBUG, format=FORMAT, datefmt=DATEFMT)
    main()
