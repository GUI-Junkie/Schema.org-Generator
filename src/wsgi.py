#!/usr/bin/python3
from wsgiref import simple_server
from controller import app


def run(app, host='localhost', port=8000):
    # Initialize the server deamon
    app._httpd = simple_server.make_server(host, port, app.__call__)
    print("Serving on port {0}...".format(port))

    # Start the server
    app._httpd.serve_forever()


if __name__ == "__main__":
    from os import chdir

    print('Schema Controller - main')

    # Change the base dir to where this __file__ is located
    # Needed for testing
    FILE_NAME = 'run.py'
    if __file__ != FILE_NAME:
        BASE_DIR = __file__[:__file__.index(FILE_NAME)]
        chdir(BASE_DIR)

    try:
        # This will setup the server and start the serve_forever() loop
        # This will block the script until the serve_forever() loop is interrupted
        run(app)

    except KeyboardInterrupt:
        # Silence KeyboardInterrupt exception
        pass
    except Exception as e:
        print(e)
        exit(-1)
