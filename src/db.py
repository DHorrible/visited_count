import redis

class DB:
    def __init__(self, cfg=None):
        if cfg is None:
            cfg = {
                'host': 'localhost',
                'port': 6379,
                'db': 0,
                'password': None,
                'socket_timeout': 1
            }
        self._conn = redis.Redis(**cfg)
    def get_conn(self):
        return self._conn
