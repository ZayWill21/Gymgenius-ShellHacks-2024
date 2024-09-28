from datetime import datetime

class gg_Handler:
    def __init__(self, req_type=None, response=None) -> None:
        self.req_type = req_type
        self.response = response
        self.log_to_file()

    def give(self, req_type, response):
        self.req_type = req_type
        self.response = response
        self.log_to_file()
        return response.choices[0].message.content

    def log_to_file(self):
        if self.req_type is None or self.response is None:
            return
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current time
        with open("api/log.txt", "a") as log_file:  # Open the log file in append mode
            log_file.write(f"{timestamp} - TYPE: {self.req_type}\nRESP: {self.response}\n\n")  # Log the output
