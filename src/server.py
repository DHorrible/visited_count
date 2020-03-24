#!/usr/bin/env python3

import os
import re
import json
import time
import http
import bisect
import urllib.parse
import logging as log

import src.db as db
import src.utility as utility

drv = None


def visited_domains(handler):
    global drv
    ret = list()
    conn = drv.get_conn()

    query = urllib.parse.urlparse(handler.path).query
    if re.match(r'^from=[0-9]+&to=[0-9]+$', query) is None:
        return http.HTTPStatus.BAD_REQUEST, 'An query is not matched with `from=<natural_number>&to=<natural_number>`', dict()
    query_val = re.sub(r'(from|to)=', '', query).split('&')
    query_val[0] = int(query_val[0])
    query_val[1] = int(query_val[1])
    if query_val[0] > query_val[1]:
        return http.HTTPStatus.BAD_REQUEST, 'The value of the `from` less or equal the value of the `to`', dict()

    keys = conn.keys('*')
    for key in keys:
        raw_val = conn.lrange(key, 0, -1)
        val = [int(x.decode('utf-8')) for x in raw_val]
        i = bisect.bisect_left(val, query_val[0])
        if i == len(val):
            continue
        elif val[i] == query_val[0] or val[i] <= query_val[1]:
            ret.append(key.decode('utf-8'))

    return http.HTTPStatus.OK, None, {'domains': ret}


def visited_links(handler):
    global drv
    conn = drv.get_conn()

    conent_header = handler.headers.get('Content-Length')
    if conent_header is None:
        return http.HTTPStatus.PARTIAL_CONTENT, 'The request does not contain the `Content-Length` header', dict()
    content_length = int(conent_header)
    post_data = ''
    try:
        post_data = json.loads(handler.rfile.read(content_length).decode('utf-8'))
    except json.decoder.JSONDecodeError:
        return http.HTTPStatus.PARTIAL_CONTENT, 'The json is not correct', dict()
    links = post_data.get('links')
    if links is None:
        return http.HTTPStatus.PARTIAL_CONTENT, 'The json body does not contain the `links` attribute (links array)', dict()

    now = int(time.time())
    for link in links:
        conn.rpush(link, now)

    return http.HTTPStatus.OK, None, dict()


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
    filename = os.getenv('ROOT_DIR')
    if filename is None:
        filename = 'server.log'
    else:
        filename += '/server.log'
    log.basicConfig(**{
        'filename': filename,
        'level': log.DEBUG,
        'format': '%(asctime)s - |%(levelname)s|: %(message)s'
    })


def run(host, port):
    global drv

    set_log()
    drv = db.DB()
    if drv.get_conn() == None:
        log.error('Redis has not bean configurated')
        return
    log.info('Redis has bean configurated')

    log.info('Starting server...\n')
    server = utility.Server('localhost', port, utility.HttpHandler)
    set_routes(server.get_handler())
    try:
        server.start()
    except KeyboardInterrupt:
        pass

    log.info('Stoping server...\n')
    server.stop()

    log.info('Creating snapshot...\n')
    drv.get_conn().save()
    log.info('Snapshot has bean created\n')


if __name__ == '__main__':
    from sys import argv

    host = 'localhost'
    port = 8080
    if len(argv) == 2:
        host = str(argv[1])
    if len(argv) == 3:
        try:
            port = int(argv[2])
        except ValueError:
            print('Error: Port should be a number!')
            exit(1)
    run(host, port)
else:
    run('localhost', 8080)
