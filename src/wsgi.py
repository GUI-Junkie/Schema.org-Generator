#!/usr/bin/python3
from controller import app


if __name__ == "__main__":
    from os import chdir

    print('Schema Controller - main')

    # Change the base dir to where this __file__ is located
    # Needed for testing
    # FILE_NAME = 'wsgi.py'
    FILE_NAME = __file__[__file__.rindex("/") + 1:]
    if __file__ != FILE_NAME:
        BASE_DIR = __file__[:__file__.index(FILE_NAME)]
        chdir(BASE_DIR)

    try:
        # This will setup the server and start the serve_forever() loop
        # This will block the script until the serve_forever() loop is interrupted
        app.run(cloud=True)

    except KeyboardInterrupt:
        # Silence KeyboardInterrupt exception
        pass
    except Exception as e:
        print(e)
        exit(-1)
