import redis

default_db_cfg = {
	'host': 'localhost',
	'port': 6379,
	'db': 0,
	'password': None,
	'socket_timeout': 1
}

def cfg(db_cfg=default_db_cfg):
	return redis.Redis(**db_cfg)
