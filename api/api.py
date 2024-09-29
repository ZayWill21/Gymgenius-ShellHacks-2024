from flask.cli import load_dotenv
from openai import OpenAI
from .gg_handler import gg_Handler
import os

load_dotenv()
class API:
    def __init__(self) -> None:
        key  = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(
            api_key=str(key)
        )  
        self.rspn_handler = gg_Handler()
    
    def send_request(self, req_type, crafted_request):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": crafted_request}
            ]
        )
        return self.rspn_handler.give(req_type, response)
