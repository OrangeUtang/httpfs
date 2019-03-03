import socket
import httpfs
import click
import os


# used path to dir = D:\School_Stuff\Python_Stuff\PythonHttpfs\workdir
@click.group()
def cli():
    pass


@cli.command()
@click.option('-v', '--verbose', is_flag=True, help="Prints debugging messages")
@click.option('-p', '--port', default=8080, required=False,
              help="Specifies the port number that the server will listen and serve at.\n Default is 8080.")
@click.option('-d', '--path', default=os.getcwd(), required=False, type=str,
              help="Specifies the directory that the server will use to read/write requested files.\n Default is the current directory when launching the application.")
def get(verbose, port, path):
    """
    httpfs is a simple file server.
    Usage: httpfs [-v] [-p PORT] [-d PATH-TO-DIR]
    """

    # validate the arguments
    if not os.path.exists(path):
        print("Directory could not be found.")

    # next create a socket object
    s = socket.socket()
    print("Socket successfully created")

    s.bind(('', port))
    print("socket binded to %s" % port)

    # put the socket into listening mode
    s.listen()
    print("socket is listening")

    # a forever loop until we interrupt it or
    # an error occurs
    while True:
        # Establish connection with client.
        c, addr = s.accept()
        print('Got connection from', addr)

        content = c.recv(32)
        while len(content):
            content = c.recv(32)

        # TODO make the connection send back the response
        # send a thank you message to the client.
        c.send('Thank you for connecting')

        # Close the connection with the client
        c.close()


if __name__ == '__main__':
    cli()
