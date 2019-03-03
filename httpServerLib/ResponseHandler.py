from httpServerLib import RequestHandler


class ResponseHandler:

    def __init__(self, RequestHandler):
        self.response_code = RequestHandler.response_code
        self.response_msg = RequestHandler.response_msg
        self.content = RequestHandler.content

    def to_string(self):
        Http_response = f"HTTP/1.0 {self.response_code} {self.response_msg}"
        # TODO finish this
        return Http_response

    def encode_request(self):
        return self.to_string().encode()
