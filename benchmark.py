import http.client
import requests
import unittest
import time
import grequests
import urllib.request
import urllib.parse
import gevent.monkey
gevent.monkey.patch_all()


class BenchMarkTest(unittest.TestCase):

    host = 'http://sample.com'
    path = '/'
    bench_mark = {
        'http_client': [],
        'requests': [],
        'grequests': [],
        'urllib': []
    }
    NO_OF_TIMES = 20
    NO_OF_REQUESTS = 20

    def test_a_http_client(self):
        for _ in range(self.NO_OF_TIMES):
            start = time.time()
            for _ in range(self.NO_OF_REQUESTS):
                if self.host.startswith("http://"):
                    connection = http.client.HTTPConnection(self.host[7:])
                else:
                    connection = http.client.HTTPSConnection(self.host[8:])
                connection.request('GET', self.path)
                response = connection.getresponse()
                connection.close()
            end = time.time()
            total = end - start
            self.bench_mark['http_client'].append(total)

    def test_b_requests(self):
        for _ in range(self.NO_OF_TIMES):
            start = time.time()
            for _ in range(self.NO_OF_REQUESTS):
                connection = requests.get('{}{}'.format(self.host, self.path))
                response = connection.text
            end = time.time()
            total = end - start
            self.bench_mark['requests'].append(total)

    def test_c_grequests(self):
        for _ in range(self.NO_OF_TIMES):
            start = time.time()
            for _ in range(self.NO_OF_REQUESTS):
                connection = grequests.get('{}{}'.format(self.host, self.path))
                response = grequests.map([connection])[0].text
            end = time.time()
            total = end - start
            self.bench_mark['grequests'].append(total)

    def test_d_urllib(self):
        for _ in range(self.NO_OF_TIMES):
            start = time.time()
            for _ in range(self.NO_OF_REQUESTS):
                f = urllib.request.urlopen('{}{}'.format(self.host, self.path))
                response = f.read().decode('utf-8')
            end = time.time()
            total = end - start
            self.bench_mark['urllib'].append(total)

    def test_e_response(self):
        for i in range(0, self.NO_OF_TIMES + 1):
            message = "{:*^12}\t".format("") if i == 0 else "{}".format(i)
            print(message, end='\t')

        print("\n")
        for i in range(0, self.NO_OF_TIMES + 1):
            print('----', end='----')

        print("\n")
        for key, values in self.bench_mark.items():
            print("{:*^12}   ".format(key), end='\t')
            for val in values:
                print("{0:.3f}".format(val), end='\t')
            print("\n")

        print("\n")
        print("\n")
        print("Response:")
        print("\n")
        for key, values in self.bench_mark.items():
            print("{:*^12}   ".format(key), end='\t')
            print(sum(values)/len(values), end='\n')
