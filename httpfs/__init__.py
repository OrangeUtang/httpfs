import socket
from httpServerLib.RequestHandler import RequestHandler
from httpServerLib.ResponseHandler import ResponseHandler
import click
import os


@click.command()
@click.option('-v', '--verbose', is_flag=True, help="Prints debugging messages")
@click.option('-p', '--port', default=8080, required=False,
              help="Specifies the port number that the server will listen and serve at.\n Default is 8080.")
@click.option('-d', '--path', default=os.getcwd(), required=False, type=str,
              help="Specifies the directory that the server will use to read/write requested files.\n Default is the current directory when launching the application.")
def cli(verbose, port, path):
    """
    httpfs is a simple file server.Usage: httpfs [-v] [-p PORT] [-d PATH-TO-DIR]
    """

    if verbose:
        print(port)
        print(path)

    # validate the arguments
    if not os.path.exists(path) and verbose:
        print("Directory could not be found.")

    # next create a socket object
    s = socket.socket()
    if verbose:
        print("Socket successfully created")

    host = "localhost"
    s.bind((host, port))

    if verbose:
        print("socket binded to %s" % port)

    # put the socket into listening mode
    s.listen(5)
    if verbose:
        print("socket is listening")

    while 1:
        c, addr = s.accept()
        print('Got connection from', addr)

        content = c.recv(4096)
        # read request
        req_hand = RequestHandler(content, path)

        if verbose:
            print(f"{req_hand.method} {req_hand.response_code} {req_hand.response_msg}")

        # create response
        resp_handler = ResponseHandler(req_hand)

        # send response
        c.sendall(resp_handler.encode_request())
        c.close()


if __name__ == '__main__':
    cli()
