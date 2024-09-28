from openai import OpenAI, OpenAIError
import pandas as pd
from .presets import Presets


class API:
    def __init__(self) -> None:
        self.client = OpenAI()  # Defaults to os.environ.get("OPENAI_API_KEY")
        self.details = ""
        self.prompt = f"""   
            Return a table in json format for {self.details}.
            Here is a sample table: {Presets.get_table_example()}
        """
    
    def test(self):
       # response = self.client.chat.completions.create(
        #model="gpt-4o-mini",
        #messages=[
        #    {"role": "user", "content": self.prompt}
        #]
        #)

        print(self.prompt)



