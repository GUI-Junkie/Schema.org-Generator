Controller
==========

.. automodule:: controller
    :members:

Starting the server at default port 8000
========================================

The Application Server can be started directly from the command line

.. code-block:: bash

    computer:~$ ./controller.py

or

.. code-block:: bash

    computer:~$ python3 controller.py

Starting the server at another port
===================================

A number of Application Servers can be started to serve at different ports.

.. code-block:: bash

    computer:~$ ./controller.py 8001 &

or

.. code-block:: bash

    computer:~$ python3 controller.py  8001 &

Shutting down the server
========================

The server can be shut down from a browser.

.. code-block:: http

    http://localhost:port/quit

or using Python

.. code-block:: python

    from urllib.error import URLError
    from urllib.request import urlopen

    try:
        urlopen('http://localhost:{0}/quit'.format(port))
    except URLError:
        pass

Restarting the server
=====================

The server can be shut down from a browser.

.. code-block:: http

    http://localhost:port/restart

or using Python

.. code-block:: python

    from urllib.error import URLError
    from urllib.request import urlopen

    try:
        urlopen('http://localhost:{0}/restart'.format(port))
    except URLError:
        pass
