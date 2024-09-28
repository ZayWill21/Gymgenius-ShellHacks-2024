from .gg_datatype import gg_Datatype

class gg_Request():
    def __init__(self) -> None:
        self.prompt = None
        self.datatype = None    
        self.api = None
        self.last_response = None

    def __init__(self, prompt, datatype, api):
        self.prompt = prompt
        self.datatype = datatype    
        self.api = api
        self.last_response = None

    def make_request(self):
        req_string = self.prompt + " and output it as a " + gg_Datatype.to_string(self.datatype) + " and follow the format given in this example for your output " + gg_Datatype.get_preset(self.datatype)
        self.last_response = self.api.send_request(self.datatype, req_string)