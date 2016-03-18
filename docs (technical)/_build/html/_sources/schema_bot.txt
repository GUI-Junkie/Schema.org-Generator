Schema bot
==========

.. automodule:: schema_bot
    :members:

Starting the bot
================

.. code-block:: bash

    computer:~$ ./schema_bot.py

or

.. code-block:: bash

    computer:~$ python3 schema_bot.py

Restarting the server(s)
========================

To restart the server(s), the ``restart(port)`` function should be called for each port as shown below
If the ports are consecutive, a ``for-loop`` can be used, of course.

This code is, naturally, inside the ``schema_bot.py`` file

.. code-block:: python

    if __name__ == "__main__":
        from os import chdir

        print('Schema Bot - main')

        # Change the base dir to where this __file__ is located
        # Same location as the Hierarchy.pickle file
        FILE_NAME = 'schema_bot.py'
        if __file__ != FILE_NAME:
            BASE_DIR = __file__[:__file__.index(FILE_NAME)]
            chdir(BASE_DIR)

        # Start the Bot
        # Check if file exists
        # Check if version is correct
        b = Bot()

        # Everything happens while the bot is alive
        while b.is_alive():
            pass

        # Restart the server(s) if the pickle file has been updated
        if b.updated:
            restart(8000)   # Restart server at port 8000
            restart(8001)   # Etc
        print('Schema Bot - main finished')
