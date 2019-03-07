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
        self.parse_req()

    def parse_req(self):
        parsed_req = self.received_request.split('\r\n\r\n')

        # dividing request in head and body
        head = parsed_req[0]
        body = ''

        if len(parsed_req) > 1:
            body = parsed_req[1]

        # splitting the head to get each individual lines
        request_msg = head.split("\n")

        # extracting information from request line
        request_line = request_msg[0].split(" ")
        self.method = request_line[0]
        if request_line[1] == "/" or len(request_line) < 3:
            self.path = "\\"
        else:
            self.path = request_line[1]

        # todo delete these, they are for testing
        print(self.method)
        print(self.path)
        print(self.content)

        # assess validity of method
        if self.method != "GET" and self.method != "POST":
            self.response_code = 400
            self.response_msg = 'Bad Request'
            self.content = "error 400 Bad Request"
            return

        # check if path exists within the designated workspace
        full_path = self.work_dir + self.path
        print(full_path)

        # retrieve content for GET /
        if self.method == "GET":
            # make sure the path is /
            if self.path == "\\":

                # get all file from directory
                dir_list = os.listdir(self.work_dir)

                # start content data
                self.content = f"Files:\r\n"

                # get all the file names
                for k in dir_list:
                    self.content += f"{k}\r\n"
                return

            # retrieve content for GET / %FILE%
            else:
                # check if path exists within the designated workspace
                if not os.path.exists(full_path):
                    self.response_code = 404
                    self.response_msg = 'Not Found'
                    self.content = "error 404 File not Found"
                    return

                with open(full_path, 'r') as a_file:
                    try:
                        self.content = a_file.read()
                    except:
                        print("File can't be read.")
                return

        # retrieve content for POST / %FILE%
        if self.method == "POST":
            if len(request_line) < 3:
                self.response_code = 400
                self.response_msg = 'Bad Request'
                self.content = "error 400 Bad Request"
                return

            # try to write to the db
            with open(full_path, 'w') as a_file:
                try:
                    a_file.write(body)
                except:
                    self.response_code = 404
                    self.response_msg = 'Not Found'
                    self.content = "error 404 File not Found"
                    return
        return
