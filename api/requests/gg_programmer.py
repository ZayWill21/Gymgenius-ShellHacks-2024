from .gg_request import gg_Request
from .gg_datatype import gg_Datatype

class Programmer(gg_Request):
    def __init__(self, prompt, datatype, api):
        super().__init__(prompt, datatype, api)

    def make_request(self):
        req_string = "Use the following prompt in order to create a workout routine\n" + \
        "The prompt is the following: " + "\"" + self.prompt + "\"" + "\n" + \
        "Then answer that input as a " + gg_Datatype.to_string(self.datatype) + ".\n" + \
        "Use this as an example for a how to format your response " + gg_Datatype.get_preset(self.datatype)
        self.last_response = self.api.send_request(self.datatype, req_string)
        return self.last_response