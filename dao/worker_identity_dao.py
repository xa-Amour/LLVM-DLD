import logging

from pymongo import MongoClient


class BaseDao(object):

    def __init__(self, ip, port):
        self.__log = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s')
        logging.root.setLevel(level=logging.INFO)
        self.init_mongo(ip, port)

    def init_mongo(self, ip, port):
        self.client = MongoClient(ip, port)
        self.db = self.client.deadlock


class WorkerIdentityDao(BaseDao):

    def __init__(self, ip='127.0.0.1', port=27017):
        super(WorkerIdentityDao, self).__init__(ip, port)
        self.__col = self.db.workerIdentify

    def get_deadlock_by_id(self, _id):
        return self.__col.find_one({'_id': _id})

    def insert_deadlock(self, _id, worker_name, inheritance_worker, worker_type):
        self.__col.insert(
            {'_id': _id, 'worker_name': worker_name, 'inheritance_worker': inheritance_worker,
             'worker_type': worker_type})

    def update_deadlock(self, _id, worker_name, inheritance_worker, worker_type):
        self.__col.update({'_id': _id}, {
            '$set': {'worker_name': worker_name, 'inheritance_worker': inheritance_worker, 'worker_type': worker_type}},
                          upsert=True)

    def get_total_count(self):
        return self.__col.find().count()