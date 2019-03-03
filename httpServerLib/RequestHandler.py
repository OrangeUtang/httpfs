import os


class RequestHandler:

    def __init__(self, req, work_dir):
        self.received_request = req.decode()
        self.method = ''
        self.path = ''
        self.work_dir = work_dir

        self.response_code = 200
        self.response_msg = 'OK'
        self.content = ''
        self.response = ''

    def parse_req(self):
        parsed_req = self.received_request.split('\r\n')

        # dividing request in head and body
        head = parsed_req[0]
        body = ''
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
            self.response_msg = 'Bad Request'

        # check if path exists within the designated workspace
        full_path = self.work_dir + self.path
        print(full_path)

        # retrieve content for GET /
        if self.method == "GET":
            if len(request_line) < 3:
                dir_list = os.listdir(self.work_dir)
                self.content = "Files:\r\n" + dir_list[0] + "\r\n" + dir_list[1]
                # TODO adding return statement here would probably be good

            # retrieve content for GET / %FILE%
            else:
                # check if path exists within the designated workspace
                if not os.path.exists(full_path):
                    self.response_code = 404
                    self.response_msg = 'Not Found'

                with open(full_path, 'r') as a_file:
                    try:
                        self.content = a_file.read()
                    except:
                        print("File can't be read.")
                # TODO adding return statement here would probably be good

        # retrieve content for POST / %FILE%
        if self.method == "POST":
            if len(request_line) < 3:
                self.response_code = 404
                self.response_msg = 'Not Found'
                # TODO adding return statement here would probably be good

            # try to write to the db
            with open(full_path, 'w') as a_file:
                try:
                    self.content = a_file.write(body)
                except:
                    self.response_code = 404
                    self.response_msg = 'Not Found'
                    # TODO adding return statement here would probably be good

        # TODO adding return statement here would probably be good
        # TODO headers?

