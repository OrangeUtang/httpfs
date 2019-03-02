import os


class RequestHandler:

    def __init__(self, req, work_dir):
        self.received_request = self.decode(req)
        self.method = ''
        self.path = ''
        self.work_dir = work_dir

        self.response_code = 200
        self.response_msg = 'OK'

    def decode(self, req):
        return req.decode()

    def parse_req(self):
        parsed_req = self.received_request.split('\r\n')

        # dividing request in head and body
        head = parsed_req[0]
        if len(parsed_req) > 1:
            body = parsed_req[1]

        # splitting the head to get each individual lines
        request_msg = head.split("\n")

        # extracting information from request line
        request_line = request_msg.split(" ")
        self.method = request_line[0]
        self.path = request_line[1]

        # assess validity of method
        if self.method != "GET" or self.method != "POST":
            self.response_code = 400

        # check if path exists within the designated workspace
        full_path = self.work_dir + self.path
        if not os.path.exists(full_path):
            self.response_code = 404


