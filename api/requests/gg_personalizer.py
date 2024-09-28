from .gg_request import gg_Request
from .gg_datatype import gg_Datatype

class Personalizer(gg_Request):
    def __init__(self, prompt, datatype, api):
        super().__init__(prompt, datatype, api)

    def make_request(self, options):
        req_string = "Shape the user input to allign with one of these options " + options + ".\n" + \
        "The user input is the following: " + "\"" + self.prompt + "\"" + "\n" + \
        "Then answer that input as a " + gg_Datatype.to_string(self.datatype) + ".\n" + \
        "Use this as an example for a sample response " + gg_Datatype.get_preset(self.datatype)
        self.last_response = self.api.send_request(self.datatype, req_string)
        return self.last_response
