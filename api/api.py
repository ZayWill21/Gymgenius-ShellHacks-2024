from openai import OpenAI
from .gg_handler import gg_Handler

class API:
    def __init__(self) -> None:
        self.client = OpenAI()  # Defaults to os.environ.get("OPENAI_API_KEY")
        self.rspn_handler = gg_Handler()
    
    def send_request(self, req_type, crafted_request):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": crafted_request}
            ]
        )
        self.rspn_handler.give(req_type, response)
