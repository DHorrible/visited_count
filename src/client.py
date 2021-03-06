#!/usr/bin/env python3

import http.client as http_client


def read_responce(conn):
    resp = conn.getresponse()
    return resp.status, resp.read().decode('utf-8')


def print_responce(status, resp):
    if status == -1:
        print('Error: Server has not bean sent respnace, status code is -1!')
    else:
        print(str.format('Status code is {0}:\n{1}', status, resp))


def input_number(n, fun):
    ret = list()
    i = 0
    while i < n:
        x = 0
        try:
            x = int(input())
        except KeyboardInterrupt:
            ret = [None] * n
            break
        except EOFError:
            ret = [None] * n
            break
        except ValueError:
            pass
        err = fun(x)
        if  err is not None:
            print(err)
            i -= 1
        else:
            ret.append(x)
        i += 1
    if n == 1:
        return ret[0]
    return tuple(ret)


def run(host, port, method=None, arg1=None, arg2=None):
    conn = http_client.HTTPConnection(host, port)

    if method is not None:
        if method == 'GET':
            conn.request('GET', str.format('/visited_domains?from={0}&to={1}', arg1, arg2))
        elif method == 'POST':
            conn.request('POST', '/visited_links', arg1, {
                'Content-type': 'application/json'
            })
        else:
            print('Error: Method should be "GET" or "POST"')
            return

        status, resp = read_responce(conn)
        print_responce(status, resp)
        return

    print(str.format('The client has bean connected to {0}:{1}', host, port))

    while True:
        print('Please, enter 1 for a GET request or 2 for a POST request')
        mod = input_number(1,
            lambda x: 'Error: Please enter 1 or 2!' if x != 1 and x != 2 else None
        )
        if mod is None:
            break
        elif mod == 1:
            print('Please, enter the start and end of the time interval (unix time)')
            _from, _to = input_number(2,
                lambda x: 'Error: Value shoul be above zero!' if x < 0 else None
            )
            print(_from, _to)
            conn.request('GET', str.format('/visited_domains?from={0}&to={1}', _from, _to))
        elif mod == 2:
            print('Please, enter a body {"links": [...]}')
            try:
                body = input()
            except KeyboardInterrupt:
                break
            conn.request('POST', '/visited_links', body, {
                'Content-type': 'application/json'
            })

        status, resp = read_responce(conn)
        print_responce(status, resp)


if __name__ == '__main__':
    from sys import argv

    host = 'localhost'
    port = 8080
    method = None
    arg1 = None
    arg2 = None
    if len(argv) == 2:
        host = str(argv[1])
    if len(argv) >= 3:
        try:
            port = int(argv[2])
        except ValueError:
            print('Error: Port should be a number!')
            exit(1)
    if len(argv) >= 4:
        method = str(argv[3])
        if method == 'GET':
            if len(argv) != 6:
                print('Error: A GET request should contains two args (are time)!')
                exit(1)
            try:
                arg1 = int(argv[4])
                arg2 = int(argv[5])
            except ValueError:
                print('Error: Arguments should be a number!')
                exit(1)
        elif method == 'POST':
            if len(argv) != 5:
                print('Error: A POST request should contains one arg (is body)!')
                exit(1)
            arg1 = argv[4]
        else:
            print('Error: Method should be "GET" or "POST"')
            exit(1)

    run(host, port, method, arg1, arg2)
else:
    run('localhost', 8080)
