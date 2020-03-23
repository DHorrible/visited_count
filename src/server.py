import os
import logging as log

import src.db as db
import src.utility as utility

drv = None

def visited_domains(handler):
    global drv
    print('visited_domains')
    return dict()

def visited_links(handler):
    global drv
    print('visited_links')
    return dict()

def set_routes(handler):
    handler.route(handler,
        'GET',
        '/visited_domains',
        visited_domains
    )
    handler.route(handler,
        'POST',
        '/visited_links',
        visited_links
    )

def set_log():
    filename = os.getenv("ROOT_DIR")
    if filename is None:
        filename = "server.log"
    else:
        filename += "/server.log"
    log.basicConfig(**{
        'filename': filename,
        'level': log.INFO,
        'format': '%(asctime)s - |%(levelname)s|: %(message)s'
    })

def run(host='localhost', port=8080):
    global drv

    set_log()
    drv = db.DB()
    if drv.get_conn() == None:
        log.error('Redis has not bean configurated')
        return
    log.info('Redis has bean configurated')

    log.info('Starting server...\n')
    server = utility.Server('localhost', port, utility.HttpHandler, log)
    set_routes(server.get_handler())
    try:
        server.start()
    except KeyboardInterrupt:
        pass
    log.info('Stoping server...\n')
    server.stop()

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 3:
        host = str(argv[1])
        port = int(argv[2])
        run(host, port)
    else:
        run()
else:
    run()
