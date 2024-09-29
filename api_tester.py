from api.api import API
from api.requests.gg_personalizer import Personalizer, gg_Datatype
from api.requests.gg_programmer import Programmer

api = API()
chatter = Personalizer("I want to gain muscle and look bigger like a body builder", gg_Datatype.conversation, api)
conversation = chatter.make_request("Bulk, cut, tone")

proggy = Programmer(conversation, gg_Datatype.table, api)
de = proggy.make_request()

import json
import re

try:
    # Assume de.choices[0].message.content contains the response text
    raw_content = de

    # Use regex to extract JSON portion from the content
    json_match = re.search(r"\{.*\}", raw_content, re.DOTALL)

    if json_match:
        # Extract the matched JSON string
        json_content = json_match.group(0)

        # Parse the JSON content
        workout_plan = json.loads(json_content)

        # Print the parsed JSON for confirmation
        print(json.dumps(workout_plan, indent=4))
    else:
        print("No valid JSON found in the content.")

except json.JSONDecodeError as e:
    print(f"JSONDecodeError: {e}")
    print("Raw content that caused the error:", raw_content)
