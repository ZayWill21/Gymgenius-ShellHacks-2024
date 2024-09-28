from .gg_datatype import gg_Datatype

class gg_Request():
    def __init__(self) -> None:
        self.prompt = None
        self.datatype = None    
        self.api = None

    def __init__(self, prompt, datatype, api):
        self.prompt = prompt
        self.datatype = datatype    
        self.api = api

    def make_request(self):
        req_string = self.prompt + " and output it as " + gg_Datatype.get_preset(self.datatype)
        self.api.send_request(self.datatype, req_string)