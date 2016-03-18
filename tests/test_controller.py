#!/usr/bin/python3
from pstats import Stats
from unittest import TestCase, main
from cProfile import run, Profile
from http import client
from time import sleep
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen
from subprocess import Popen, PIPE

TEST_DIR = '{0}tests/test_files/'.format(__file__[:__file__.index('tests')])


def get_connection():
    sleep(1)  # It's necessary to wait a second for Popen or /restart to do it's thing
    try:
        urlopen('http://localhost:8000')
    except URLError:
        return False
    return True


class Test(TestCase):
    changed_files = False
    # changed_files = True

    cli = None
    is_running = None
    profiler = None

    @classmethod
    def setUpClass(cls):
        cls.profiler = Profile()
        cls.profiler.enable()

        # Check if the server is running
        pipe1 = Popen(["ps", "aux"], stdout=PIPE)
        pipe2 = Popen(["grep", "doController.py"], stdin=pipe1.stdout, stdout=PIPE)
        pipe1.stdout.close()

        pipe1 = Popen(["grep", "-v", "grep"], stdin=pipe2.stdout, stdout=PIPE)
        pipe2.stdout.close()

        procs = pipe1.communicate()[0]
        # If the server is running, we keep it running
        if b"doController.py" in procs:
            urlopen('http://localhost:8000/restart')
            cls.is_running = True
        else:
            # If the server is not running, start it for the duration of the tests
            Popen(['python3', '{0}src/controller.py'.format(__file__[:__file__.index('tests')])])

        i = 0
        while not get_connection() and i < 100:
            i += 1
        cls.cli = client.HTTPConnection('localhost:8000', timeout=100)

    @classmethod
    def tearDownClass(cls):
        if cls.is_running:
            return
        urlopen('http://localhost:8000/quit')
        cls.cli.close()
        p = Stats(cls.profiler)
        p.strip_dirs()
        p.sort_stats('cumtime')
        # p.print_stats()
        # print("\n--->>>")

    def testURLOpen(self):
        with urlopen('http://localhost:8000') as f:
            txt = f.readall()
        self.assertIn(b'/Thing', txt, "Oh, bloody hell!")

    def testQuery(self):
        d = {'DateTime': '', 'URL': '', 'Text': '', 'next_element': 'ActionStatusType'}
        t = d['next_element']
        self.assertEqual(t, 'ActionStatusType', 'testQuery: {0}'.format(t))

    def testAjax(self):
        test_file = '{0}ajax.html'.format(TEST_DIR)
        with open(test_file) as f:
            txt_html = f.read()

        data = {'next_element': 'ActionStatusType',
                'id': 'LoseAction_actionStatus_ActionStatusType'}
        data = bytes(urlencode(data).encode())
        with urlopen('http://localhost:8000/ActionStatusType', data) as f:
            txt = f.readall().decode()

        # If the output doesn't coincide, there may be another version of Schema.org
        if self.changed_files:
            with open(test_file, 'w') as f:
                f.write(txt)
        self.assertEqual(txt, txt_html, 'test_Ajax')

if __name__ == "__main__":
    # Try to connect to the server
    # If a connection can be made, tell the server to restart
    try:
        cli = client.HTTPConnection('localhost:8000', timeout=1)
        cli.connect()
        cli.request("GET", '/restart')
        cli.getresponse()
        sleep(0.1)
    except ConnectionRefusedError:
        pass

    run(main())

# python3 -m cProfile -s cumtime doController.py
# python3 -m cProfile -s cumtime doController.py | grep controller
# python3 -m cProfile -s cumtime doController.py | grep schema
