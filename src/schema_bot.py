#!/usr/bin/python3
"""
Bot for fetching the |Schema.org| |external_link| full hierarchy to generate the ``Hierarchy.pickle`` file

The Bot class will check for the existence of the pickle file and for the version

* If the file doesn't exist, it will be generated by the Bot

* If the file is outdated, it will be updated by the Bot

After updating the ``Hierarchy.pickle`` file, a new static ``index.html`` will be generated

The Bot should be called via a ``cron`` job every 24 hours

* The Application Server |Controller| (or Controllers) will be restarted if necessary
"""
from os import remove, makedirs
# Refer to the Readme.txt file for © copyright information
from pickle import load
from shutil import rmtree
from threading import Thread
from time import sleep
from urllib.error import URLError, HTTPError
from urllib.request import urlopen
from zlib import decompress, MAX_WBITS

from model.schema import SCHEMA_ORG
from nqparser import treat_file

HIERARCHY_FILE = 'Hierarchy.pickle'
READ_BINARY = 'rb'
WRITE = 'w'
WRITE_BINARY = 'wb'


class Bot(Thread):
    def __init__(self):
        Thread.__init__(self)
        # Public attributes
        self.debug = False  # Running locally
        self.updated = False
        self.error = None
        self.version = 0.0  # Version of Schema.org

        # Private attributes
        self._is_alive = True
        self._schemas = {}  # Dictionary for rapid access

    def run(self):
        is_dirty = False
        try:
            # First load the existing HIERARCHY_FILE
            with open(HIERARCHY_FILE, READ_BINARY) as f:
                pickle_list = load(f)
                self.version = pickle_list[0]
        except FileNotFoundError:
            # HIERARCHY_FILE is not there
            is_dirty = True

        if self.debug:
            is_dirty = True
            self.version = 0.0

        # Check the version of the Hierarchy against the known version
        i_tries = 0
        txt = None
        while i_tries < 9 and txt is None:
            i_tries += 1
            try:
                with urlopen(f'{SCHEMA_ORG}docs/releases.html') as f:
                    txt = f.read()
                if 31 == txt[0]:  # If the txt is compressed, decompress
                    txt = decompress(txt, 16 + MAX_WBITS)
            except URLError:
                # Wait a millisecond before trying again
                print('Sleeping Schema_bot... waiting for version')
                sleep(0.1)

        if txt is None:
            # Abandon ship
            self.error = 'Schema bot abandoned. Check Internet connection'
            return

        # Check the version
        # <td class="release"><a href="/version/2.1/">2.1</a><br/>sdo-ganymede<br/>(2015-08-06)</td>
        txt = txt.decode()
        ind = txt.index('class="release"')
        ind += txt[ind:].index('href="') + len('href="/version/')
        version = float(txt[ind:ind + txt[ind:].index('/')])
        if version > self.version:
            self.version = version
            is_dirty = True

        if is_dirty:
            # Get the new release all-layers.nq file
            # https://raw.githubusercontent.com/schemaorg/schemaorg/master/data/releases/3.0/all-layers.nq
            try:
                with urlopen('https://raw.githubusercontent.com/schemaorg/schemaorg/master/data/releases/'
                             f'{version}/all-layers.nq') as f:
                    txt = f.read()
            except HTTPError:
                with urlopen('https://raw.githubusercontent.com/schemaorg/schemaorg/sdo-makemake/data/releases/'
                             f'{version}/all-layers.nq') as f:
                    txt = f.read()

            with open('all-layers.nq', WRITE) as f:
                    f.write(txt.decode())

            # Delete index.html
            try:
                remove('view/index.html')
            except FileNotFoundError:
                pass

            # Delete all schemas
            rmtree('schemas/')
            makedirs('schemas/')

            # Let's do *everything*
            treat_file(version)
            self.updated = True

        self._is_alive = False

    def is_alive(self):
        return self._is_alive


def restart(port):
    try:
        urlopen(f'http://localhost:{port}/restart')
    except URLError:
        pass


if __name__ == "__main__":
    from os import chdir
    from datetime import datetime

    start_time = datetime.now()

    print('Schema Bot - main')

    # Change the base dir to where this __file__ is located
    # Same location as the Hierarchy.pickle file
    # FILE_NAME = 'schema_bot.py'
    FILE_NAME = __file__[__file__.rindex("/") + 1:]
    if __file__ != FILE_NAME:
        BASE_DIR = __file__[:__file__.index(FILE_NAME)]
        chdir(BASE_DIR)

    # Start the Bot
    # Check if file exists
    # Check if version is correct
    b = Bot()
    b.debug = True
    b.start()
    b.join()

    # Everything happens while the bot is alive
    while b.is_alive():
        pass

    # Restart the server(s) if the pickle file has been updated
    if b.updated:
        restart(8000)  # Restart server at port 8000
        # restart(8001)   # Etc
    print('Schema Bot - main finished')

    stop_time = datetime.now()
    time_delta = stop_time - start_time

    hours, remainder = divmod(time_delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    print("\nDuration:", f'{hours:02d}:{minutes:02d}:{seconds:02d} and {time_delta.microseconds} microseconds')
