from httpServerLib import RequestHandler
from datetime import date
from datetime import datetime
from datetime import timezone


class ResponseHandler:

    def __init__(self, req_handler=RequestHandler):
        self.response_code = req_handler.response_code
        self.response_msg = req_handler.response_msg
        self.content = req_handler.content

    def to_string(self):
        http_response = f"HTTP/1.0 {self.response_code} {self.response_msg}\r\n"
        http_response += f"{self.generate_time_header()}\r\n"
        http_response += f"Content-Length: {str(len(self.content))}\r\n"
        http_response += "\r\n"
        http_response += f"{self.content}"
        return http_response

    def encode_request(self):
        return self.to_string().encode()

    def generate_time_header(self):
        # getting relevant date/time
        d = date.today()
        t = datetime.now(timezone.utc)

        # extracting good format for
        day = d.strftime("%A")
        weekday = day[0:3]
        day = d.strftime("%d")
        month = d.strftime("%B")
        month = month[0:3]
        year = d.strftime("%Y")
        time = t.strftime("%H:%M:%S")

        # assembling header info
        time_header = f"Date: {weekday}, {day} {month} {year} {time} GMT"
        return time_header
