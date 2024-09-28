
class gg_Handler():
    def __init__(self, req_type, response) -> None:
        self.req_type = req_type
        self.response = response

        print(f"TYPE: {self.req_type}\nRESP: {self.response}")

    def __init__(self) -> None:
        self.req_type = ""
        self.response = ""

    def give(self, req_type, response):
        self.req_type = req_type
        self.response = response

        print(f"TYPE: {self.req_type}\nRESP: {self.response}")